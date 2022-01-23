from django.db import models
from users.models import User


class Measure(models.Model):
    name = models.CharField(
        max_length=32,
        verbose_name='measures',
        unique=True
    )


class IngredientList(models.Model):
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


class Ingredient(models.Model):
    ingredient = models.ForeignKey(
        to=IngredientList,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='ingredients',
    )
    amount = models.PositiveIntegerField(
        verbose_name='amount'
    )


class Tag(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='tags',
        unique=True
    )
    color = models.CharField(
        max_length=16,
        verbose_name='Hex codes',
        unique=True
    )
    slug = models.SlugField(
        max_length=256,
        verbose_name='slugs',
        unique=True
    )


class Recipe(models.Model):
    author = models.ForeignKey(
        to=User,
        related_name='recipies',
        verbose_name='author',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=256,
        verbose_name='recipes'
    )
    image = models.ImageField(
        upload_to='recipies/',
    )
    description = models.TextField()
    ingredients = models.ManyToManyField(
        to=Ingredient,
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        to=Tag,
        related_name='recipes'
    )
    cooking_time = models.IntegerField()


class Follow(models.Model):
    user = models.ForeignKey(
        to=User,
        related_name='follower',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        to=User,
        related_name='following',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_author_user_following'
            )
        ]

    def __str__(self) -> str:
        return (
            f'Автор: {self.author} '
            f'- Подписчик: {self.user}'
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
        related_name='favorites'
    )

    class Meta:
        models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_recipe_user_favorite'
        )
