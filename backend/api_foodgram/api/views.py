from djoser import views as djoser
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers import (IngredientSerializer, TagSerializer,  # isort:skip
                             UserSerializer)
from recipes.models import Ingredient, Tag  # isort:skip
from users.models import User  # isort:skip


class UserViewSet(djoser.UserViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = PageNumberPagination

    @action(detail=False, methods=['get'])
    def me(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, method=['get'])
    def subscriptions(self, request):
        pass

    @action(detail=True, method=['get', 'delete'])
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
