from djoser import views as djoser
from rest_framework.pagination import PageNumberPagination
from users.models import User

from .serializers import CustomUserSerializer


class UserViewSet(djoser.UserViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
