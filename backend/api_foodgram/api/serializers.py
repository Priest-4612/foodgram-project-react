from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User

FORBIDDEN_USERNAME = [
    'me', 'Me',
    'admin', 'Admin'
]
ERROR_FORBIDDEN_USERNAME = ('Использовать имя "{username}" в качестве '
                            'username запрещено.')


class MeSerializer(serializers.ModelSerializer):
    is_subscribe = serializers.SerializerMethodField()

    email = serializers.EmailField(
        max_length=150,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        max_length=150,
        required=True,
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

    def validate_username(self, value):
        if value in FORBIDDEN_USERNAME:
            raise serializers.ValidationError(
                self.ERROR_FORBIDDEN_USERNAME.format(username=value)
            )
        return value

    class Meta:
        fields = [
            'username', 'email', 'first_name', 'last_name', 'is_subscribe'
        ]
        model = User

    def get_is_subscribe(self, obj):
        user = self.context['request'].user
        return (
            user
            and obj.followed.filter(user__username=user).exists()
        )


class UserSerualizer(serializers.ModelSerializer):
    is_subscribe = serializers.SerializerMethodField()

    email = serializers.EmailField(
        max_length=150,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        max_length=150,
        required=True,
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

    def validate_username(self, value):
        if value in FORBIDDEN_USERNAME:
            raise serializers.ValidationError(
                self.ERROR_FORBIDDEN_USERNAME.format(username=value)
            )
        return value

    class Meta:
        fields = [
            'username', 'email', 'first_name', 'last_name', 'is_subscribe'
        ]
        model = User

    def get_is_subscribe(self, obj):
        user = self.context['request'].user
        return (
            user
            and obj.followed.filter(user__username=user).exists()
        )


class RegisterSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=150,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        max_length=150,
        required=True,
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

    def validate_username(self, value):
        if value in FORBIDDEN_USERNAME:
            raise serializers.ValidationError(
                self.ERROR_FORBIDDEN_USERNAME.format(username=value)
            )
        return value

    class Meta:
        fields = ['username', 'email', 'first_name', 'last_name']
        model = User
