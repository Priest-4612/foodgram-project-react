from django.core.validators import MinValueValidator
from django.db import models
from users.models import User

ERROR_MIN_VALUE = 'Величина не может быть меньше {min_value}'
MIN_COOKING_TIME = 1
MIN_INGREDIENT_AMOUNT = 1


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


class CountOfIngredient(models.Model):
    ingredient = models.ForeignKey(
        to=Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='ingredients',
    )
    amount = models.PositiveIntegerField(
        verbose_name='amount',
        validators=(MinValueValidator(
            limit_value=MIN_INGREDIENT_AMOUNT,
            message=ERROR_MIN_VALUE.format(min_value=MIN_INGREDIENT_AMOUNT)
        ),)
    )

    def __str__(self):
        return (
            f'{self.ingredient.name}: {self.amount}'
            f'{self.ingredient.measurement_unit.name}'
        )


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

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    author = models.ForeignKey(
        to=User,
        related_name='recipes',
        verbose_name='author',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=256,
        verbose_name='recipes'
    )
    image = models.ImageField(
        upload_to='recipes/',
    )
    description = models.TextField()
    ingredients = models.ManyToManyField(
        to=CountOfIngredient,
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

    class Meta:
        ordering = ['-pk']


class Favorite(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_recipe_user_favorite'
        )
