# from django.shortcuts import render
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User

from .permissions import OwnerOnly, ReadOnly
# from .serializers import LoginSerializer, RegisterSerializers, UserSerializer
from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    permission_classes = [ReadOnly]
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()
    pagination_class = PageNumberPagination



# class UserViewSet(viewsets.ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     pagination_class = PageNumberPagination

#     def get_permissions(self):
#         if self.action in ['list', 'retrieve', 'create']:
#             permission_classes = [AllowAny]
#         else:
#             permission_classes = [IsAdminUser]
#         return [permission() for permission in permission_classes]

#     def post(self, request):
#         serializer = RegisterSerializers(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             data=serializer.validated_data,
#             status=status.HTTP_200_OK
#         )

#     @action(detail=False, methods=['get', 'post', 'put', 'patch'], name='me',
#             permission_classes=[OwnerOnly])
#     def me(self, request):
#         user = request.user
#         if request.method == 'GET':
#             serializer = UserSerializer(user, context={'request': request})
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#         serializer = UserSerializer(user, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data=serializer.data, status=status.HTTP_200_OK)


# class LoginView(APIView):
#     permission_classes = [AllowAny]
#     serializer_class = LoginSerializer

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
