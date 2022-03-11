from djoser import views as djoser
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers import (  # isort:skip
    IngredientSerializer, RecipeSerializer,
    SubscriptionSerializer, TagSerializer, UserSerializer
)
from recipes.models import Ingredient, Recipe, Tag  # isort:skip
from users.models import User  # isort:skip


class UserViewSet(djoser.UserViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = PageNumberPagination

    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribing__subscriber=request.user)
        page = self.paginate_queryset(queryset)
        if page is None:
            serializer = SubscriptionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = SubscriptionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'delete'])
    def subscribe(self, request, id):
        pass


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [AllowAny]
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [AllowAny]
    pagination_class = None
    http_method_names = ['get']


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
