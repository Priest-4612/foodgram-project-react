from djoser import views as djoser
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from users.models import User

from .serializers import CustomUserSerializer


class UserViewSet(djoser.UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()
    pagination_class = PageNumberPagination

    @action(detail=False, methods=['get'])
    def me(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
