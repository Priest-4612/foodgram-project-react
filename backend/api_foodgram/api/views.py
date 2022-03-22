from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from djoser import views as djoser
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter  # isort:skip
from api.pagination import CustomPagination  # isort:skip
from api.permissions import IsOwnerOrAdmin  # isort:skip
from api.serializers import (  # isort:skip
    FavoriteSerializer, IngredientSerializer, RecipeSerializer,
    ShortRecipeSerivalizer, ShoppingCardSerializer, SubscriptionSerializer,
    SubscriberSerializer, TagSerializer, UserSerializer
)
from recipes.models import (  # isort:skip
    Favorite, Ingredient, Recipe, RecipeIngredient, ShoppingCart, Tag
)
from users.models import Subscribe, User  # isort:skip


class UserViewSet(djoser.UserViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = CustomPagination

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribing__subscriber=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, id=None):
        subscriber = request.user
        author = get_object_or_404(User, pk=id)
        if request.method == 'POST':
            serializer = SubscriberSerializer(
                data={"author": author.id},
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = SubscriptionSerializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        subscription = get_object_or_404(
            Subscribe,
            subscriber=subscriber,
            author=author
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None
    http_method_names = ['get']
    filter_backends = [IngredientFilter]
    search_fields = ['^name']


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all().order_by('-id')
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]
    pagination_class = CustomPagination
    filterset_class = RecipeFilter

    def item_add_or_delete(self, request, serializer, model, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            serializer = serializer(
                data={'recipe': recipe.id},
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = ShortRecipeSerivalizer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        item = get_object_or_404(
            model,
            user=user,
            recipe=recipe
        )
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        return self.item_add_or_delete(
            request=request,
            serializer=FavoriteSerializer,
            model=Favorite,
            pk=pk
        )

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        return self.item_add_or_delete(
            request=request,
            serializer=ShoppingCardSerializer,
            model=ShoppingCart,
            pk=pk
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        shopping_list = RecipeIngredient.objects.filter(
            recipe__is_in_shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit__name'
        ).order_by(
            "ingredient__name"
        ).annotate(
            Sum('amount')
        )
        content = ['Список ингредиентов для выбранных рецептов:\n\n', ]
        for index, item in enumerate(shopping_list):
            content.append(
                f'{index + 1}. {item["ingredient__name"]} ('
                f'{item["ingredient__measurement_unit__name"]}) - '
                f'{item["amount__sum"]}\n'
            )
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment;' 'filename="shopping_list.txt"'
        )
        return response
