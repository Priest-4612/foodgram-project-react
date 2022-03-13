from djoser import serializers as djoser
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Ingredient, CountOfIngredient,  # isort:skip
                            Recipe, Tag)
from users.models import Subscribe, User  # isort:skip


ERROR_SUBSCRIBE_TO_YOURSELF = 'Вы не можете подписаться на себя'
ERROR_CANNOT_SUBSCRIBE_TWICE = 'Нельзя дважды подписаться.'


class UserSerializer(djoser.UserSerializer):
    is_subscribe = serializers.SerializerMethodField()

    class Meta:
        fields = [
            'email', 'password', 'id', 'username',
            'first_name', 'last_name', 'is_subscribe'
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }
        model = User

    def get_is_subscribe(self, obj):
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and obj.subscribing.filter(subscriber=request.user).exists()
        )

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']
        read_only_fields = ['name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.ReadOnlyField(
        source='measurement_unit.name'
    )

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']
        read_only_fields = ['name', 'measurement_unit']


class CounyOfIngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )
    name = serializers.CharField(
        source='ingredient.name',
        read_only=True
    )

    class Meta:
        model = CountOfIngredient
        fields = ['id', 'name', 'measurement_unit', 'amount']
        read_only_fields = ['name', 'measurement_unit']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = CounyOfIngredientSerializer(many=True)
    author = UserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time']
        read_only_fields = ['id']
        depth = 1

    # def create(self, validated_data):
    #     tags = validated_data.pop('tags')
    #     ingredients = validated_data.pop('ingredients')
    #     recipe = Recipe.objects.create(**validated_data)

    #     for tag in tags:
    #         current_tag = Tag.objects.get(**tag)
    #         RecipeTag.objects.create(recipe=recipe, tag=current_tag)

    #     for ingredient in ingredients:
    #         current_ingredient = Ingredient.objects.get_or_create(**ingredient)
    #         RecipeIngredient.objects.create(recipe=recipe,
    #                                         tag=current_ingredient)

    #     return recipe

    def get_is_favorited(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
        return False


class SubscriptionRecipeSerivalizer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']
        read_only_fields = ['id', 'name', 'image', 'cooking_time']


class SubscriptionSerializer(UserSerializer):
    recipes = SubscriptionRecipeSerivalizer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['recipes', 'recipes_count']

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscriberSerializer(serializers.ModelSerializer):
    subscriber = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Subscribe
        fields = ['subscriber', 'author']
        validators = [
            UniqueTogetherValidator(
                queryset=Subscribe.objects.all(),
                fields=['subscriber', 'author'],
                message=ERROR_CANNOT_SUBSCRIBE_TWICE
            )
        ]

    def validate_author(self, value):
        request = self.context.get('request')
        if not request.user == value:
            return value
        raise serializers.ValidationError(
            ERROR_SUBSCRIBE_TO_YOURSELF
        )
