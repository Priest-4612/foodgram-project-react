from djoser import views as djoser
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from users.models import User

from .permissions import OwnerOnly, ReadOnly
from .serializers import CustomUserSerializer


class UserViewSet(djoser.UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [ReadOnly]
        elif self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'me':
            permission_classes = [OwnerOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get', 'post', 'put', 'patch'])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = CustomUserSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        serializer = CustomUserSerializer(user, data=request.data,
                                          partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
