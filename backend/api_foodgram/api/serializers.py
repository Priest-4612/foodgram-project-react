from djoser import serializers as djoser
from recipes.models import Follow, Tag
from rest_framework import serializers
from users.models import User


class UserSerializer(djoser.UserSerializer):
    is_subscribe = serializers.SerializerMethodField()
    password = serializers.CharField(
        write_only=True
    )
    id = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        fields = [
            'email', 'password', 'id', 'username',
            'first_name', 'last_name', 'is_subscribe'
        ]
        model = User

    def get_is_subscribe(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        user = request.user
        return Follow.objects.filter(author=obj, user=user).exists()

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
