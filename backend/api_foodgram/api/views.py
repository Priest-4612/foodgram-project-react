# from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User

from .serializers import MeSerializer, UserSerualizer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerualizer
    queryset = User.objects.all()

    @action(detail=False, methods=['get', 'post', 'put', 'patch'], name='me')
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = MeSerializer(user, context={'request': request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        serializer = MeSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
