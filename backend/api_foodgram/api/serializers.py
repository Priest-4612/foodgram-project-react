# from django.contrib.auth import authenticate
# from django.contrib.auth.password_validation import validate_password
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User

FORBIDDEN_USERNAME = [
    'me', 'Me',
    'admin', 'Admin'
]
ERROR_FORBIDDEN_USERNAME = ('Использовать имя "{username}" в качестве '
                            'username запрещено.')


class CustomUserSerializer(UserSerializer):
    is_subscribe = serializers.SerializerMethodField()
    id = serializers.IntegerField(
        read_only=True
    )

    email = serializers.EmailField(
        required=True,
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(
        max_length=150,
        required=True
    )
    last_name = serializers.CharField(
        max_length=150,
        required=True
    )

    class Meta:
        fields = [
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribe'
        ]
        model = User

    def get_is_subscribe(self, obj):
        user = self.context['request'].user
        return (
            user
            and obj.followed.filter(user__username=user).exists()
        )

    def validate_username(self, value):
        if value in FORBIDDEN_USERNAME:
            raise serializers.ValidationError(
                self.ERROR_FORBIDDEN_USERNAME.format(username=value)
            )
        return value


# class DefaultUserSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         required=True,
#         max_length=150,
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#     username = serializers.CharField(
#         required=True,
#         max_length=150,
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#     first_name = serializers.CharField(
#         max_length=150,
#         required=True
#     )
#     last_name = serializers.CharField(
#         max_length=150,
#         required=True
#     )

#     def validate_username(self, value):
#         if value in FORBIDDEN_USERNAME:
#             raise serializers.ValidationError(
#                 self.ERROR_FORBIDDEN_USERNAME.format(username=value)
#             )
#         return value


# class RegisterSerializers(DefaultUserSerializer):
#     password = serializers.CharField(
#         max_length=150,
#         write_only=True,
#         required=True,
#         validators=[validate_password]
#     )

#     class Meta:
#         fields = ['username', 'email', 'first_name', 'last_name', 'password']
#         model = User

#     def create(self, validated_data):
#         user = User.objects.create(
#             email=validated_data['email'],
#             username=validated_data['username'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name']
#         )
#         user.set_password(self, raw_password=validated_data['password'])
#         user.save()
#         return user


# class UserSerializer(DefaultUserSerializer):
#     is_subscribe = serializers.SerializerMethodField()
#     id = serializers.IntegerField(
#         read_only=True
#     )

#     class Meta:
#         fields = [
#             'email', 'id', 'username',
#             'first_name', 'last_name', 'is_subscribe'
#         ]
#         model = User

#     def get_is_subscribe(self, obj):
#         user = self.context['request'].user
#         return (
#             user
#             and obj.followed.filter(user__username=user).exists()
#         )


# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField(
#         max_length=150,
#         write_only=True,
#         required=True,
#     )
#     password = serializers.CharField(
#         max_length=150,
#         write_only=True,
#         required=True
#     )
#     username = serializers.CharField(
#         max_length=255,
#         read_only=True
#     )

#     def validate(self, data):
#         email = data.get('email', None)
#         password = data.get('password', None)

#         if email is None:
#             raise serializers.ValidationError(
#                 'An email address is required to log in.'
#             )

#         if password is None:
#             raise serializers.ValidationError(
#                 'A password is required to log in.'
#             )

#         user = authenticate(username=email, password=password)

#         if user is None:
#             raise serializers.ValidationError(
#                 'A user with this email and password was not found.'
#             )

#         if not user.is_active:
#             raise serializers.ValidationError(
#                 'This user has been deactivated.'
#             )

#         return {
#             'username': user.username
#         }
