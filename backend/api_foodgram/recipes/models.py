from django.core.validators import MinValueValidator
from django.db import models
from users.models import User

ERROR_MIN_VALUE = 'Величина не может быть меньше {min_value}'
MIN_COOKING_TIME = 1
MIN_INGREDIENT_AMOUNT = 1


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='tags',
        unique=True
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Hex codes',
        unique=True
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='slugs',
        unique=True
    )

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.name}'


class Measure(models.Model):
    name = models.CharField(
        max_length=32,
        verbose_name='measures',
        unique=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='ingredients'
    )
    measurement_unit = models.ForeignKey(
        to=Measure,
        on_delete=models.CASCADE,
        verbose_name='measurement unit',
        related_name='ingredient_list'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        max_length=256,
        verbose_name='recipes'
    )
    image = models.ImageField(
        upload_to='recipes/',
    )
    text = models.TextField()
    ingredients = models.ManyToManyField(
        to=Ingredient,
        through='RecipeIngredient',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        to=Tag,
        related_name='recipes'
    )
    cooking_time = models.PositiveIntegerField(
        validators=(MinValueValidator(
            limit_value=MIN_COOKING_TIME,
            message=ERROR_MIN_VALUE.format(min_value=MIN_COOKING_TIME)
        ),)
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient'
    )
    ingredient = models.ForeignKey(
        to=Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
    )
    amount = models.PositiveIntegerField(
        verbose_name='amount',
        validators=(MinValueValidator(
            limit_value=MIN_INGREDIENT_AMOUNT,
            message=ERROR_MIN_VALUE.format(min_value=MIN_INGREDIENT_AMOUNT)
        ),)
    )

    class Meta:
        ordering = ['-pk']
        constraints = [
            models.UniqueConstraint(
                name='unique_ingredient_for_recipe',
                fields=('recipe', 'ingredient',),
            )
        ]

    def __str__(self):
        return (
            f'{self.ingredient.name}: {self.amount}'
            f'{self.ingredient.measurement_unit.name}'
        )


class Favorite(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='is_favorited'
    )

    class Meta:
        ordering = ['-pk']
        models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_recipe_user_favorite'
        )

    def __str__(self):
        return (
            f'Пользователь: {self.user.username} - '
            f'Рецепт в избранном {self.recipe.name}')


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='buyer'
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='buy'
    )

    class Meta:
        ordering = ['-pk']
        models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_recipe_in_shopping_cart'
        )

    def __str__(self):
        return (
            f'Пользователь: {self.user.username} - '
            f'Рецепт в корзине {self.recipe.name}')
