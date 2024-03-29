from djoser import serializers as djoser
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Favorite, Ingredient, Measure,  # isort:skip
                            Recipe, RecipeIngredient, ShoppingCart, Tag)
from users.models import Subscribe, User  # isort:skip


ERROR_SUBSCRIBE_TO_YOURSELF = 'Вы не можете подписаться на себя'
ERROR_CANNOT_SUBSCRIBE_TWICE = 'Нельзя дважды подписаться.'
ERROR_INGREDIENT_AMOUNT = (
    'Количество ингредиента должно быть целым числом больше 1.'
)
ERROR_UNIQUE_INGREDIENTS = (
    'Проверьте, что не добавляете в рецепт один и тот же '
    'ингредиент дважды.'
)
ERROR_NO_TAG = 'Необходимо указать хоть бы один тег.'
ERROR_NOT_INT_TAG = 'Необходимо указать число соответствующее ID тега.'
ERROR_CANNOT_ADD_TWICE = 'Нельзя добвить дважды.'


class UserSerializer(djoser.UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = [
            'email', 'password', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed'
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }
        model = User

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and request.user.subscriber.filter(author=obj.id).exists()
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


class MeasureSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.ReadOnlyField(
        source='measures.name'
    )

    class Meta:
        model = Measure
        exclude = ['id']


class IngredientSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.ReadOnlyField(
        source='measurement_unit.name'
    )

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']
        read_only_fields = ['name', 'measurement_unit']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit.name'
    )
    name = serializers.CharField(
        source='ingredient.name',
        read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'name', 'measurement_unit', 'amount']


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    ingredients = RecipeIngredientSerializer(
        source='recipe_ingredient', many=True
    )
    image = Base64ImageField(max_length=None, use_url=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'author', 'tags', 'ingredients', 'image',
                  'is_favorited', 'is_in_shopping_cart', 'name',
                  'text', 'cooking_time']
        model = Recipe

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and obj.is_favorited.filter(user=request.user).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and obj.is_in_shopping_cart.filter(user=request.user).exists()
        )

    def validate(self, data):
        tags_data = self.initial_data.get('tags')
        if len(tags_data) == 0:
            raise serializers.ValidationError(ERROR_NO_TAG)
        ingredients_data = data.get('recipe_ingredient')
        all_ingredients_ids = []

        for item in ingredients_data:
            item_data = list(item.values())
            all_ingredients_ids.append(item_data[0]['id'])
            if item_data[1] < 1:
                raise serializers.ValidationError(ERROR_INGREDIENT_AMOUNT)
            if not isinstance(item_data[1], int):
                raise serializers.ValidationError(ERROR_INGREDIENT_AMOUNT)
        unique_ingredients_ids = set(all_ingredients_ids)
        if len(all_ingredients_ids) != len(unique_ingredients_ids):
            raise serializers.ValidationError(ERROR_UNIQUE_INGREDIENTS)

        return data

    def add_tags_and_ingredients(self, instance, tags, ingredients):
        instance.tags.set(tags)
        set_of_ingredients = [
            RecipeIngredient(
                recipe=instance,
                ingredient=get_object_or_404(
                    Ingredient, id=item['ingredient']['id']
                ),
                amount=item['amount']
            ) for item in ingredients
        ]
        RecipeIngredient.objects.bulk_create(set_of_ingredients)

        return instance

    def create(self, validated_data):
        tags = self.initial_data.get('tags')
        ingredients = validated_data.pop('recipe_ingredient')
        recipe = Recipe.objects.create(
            author=self.context.get('request').user,
            image=validated_data.pop('image'),
            **validated_data
        )
        return self.add_tags_and_ingredients(recipe, tags, ingredients)

    def update(self, instance, validated_data):
        tags = self.initial_data.get('tags')
        ingredients = validated_data.pop('recipe_ingredient')
        instance.ingredients.clear()
        instance.tags.clear()
        instance = self.add_tags_and_ingredients(instance, tags, ingredients)
        return super().update(instance, validated_data)


class ShortRecipeSerivalizer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']
        read_only_fields = ['id', 'name', 'image', 'cooking_time']


class SubscriptionSerializer(UserSerializer):
    recipes = ShortRecipeSerivalizer(many=True)
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


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Favorite
        fields = ['user', 'recipe']
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe'],
                message=ERROR_CANNOT_ADD_TWICE
            )
        ]


class ShoppingCardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = ShoppingCart
        fields = ['user', 'recipe']
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=['user', 'recipe'],
                message=ERROR_CANNOT_ADD_TWICE
            )
        ]
