from djoser import serializers as djoser
from recipes.models import (Follow, Ingredient, IngredientList, Recipe,
                            RecipeIngredient, RecipeTag, Tag)
from rest_framework import serializers
from users.models import User


class UserSerializer(djoser.UserSerializer):
    is_subscribe = serializers.SerializerMethodField()

    class Meta:
        fields = [
            'email', 'password', 'id', 'username',
            'first_name', 'last_name', 'is_subscribe'
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }
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
        fields = ['id', 'name', 'color', 'slug']
        read_only_fields = ['name', 'color', 'slug']


class IngredientListSerializer(serializers.ModelSerializer):

    class Meta:
        model = IngredientList
        fields = ['id', 'name', 'measurement_unit']


class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )
    name = serializers.CharField(
        source='ingredient.name',
        read_only=True
    )

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit', 'amount']
        read_only_fields = ['name', 'measurement_unit']


class RecipeSerializer(serializers.ModelSerializer):
    # tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True)
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

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        for tag in tags:
            current_tag = Tag.objects.get(**tag)
            RecipeTag.objects.create(recipe=recipe, tag=current_tag)

        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get_or_create(**ingredient)
            RecipeIngredient.objects.create(recipe=recipe,
                                            tag=current_ingredient)

        return recipe

    def get_is_favorited(self, obj):
        return False

    def get_is_in_shopping_cart(self, obj):
        return False
