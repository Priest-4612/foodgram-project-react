from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Measure(models.Model):
    name = models.CharField(
        max_length=32,
        verbose_name='measures',
        unique=True,
    )


class IngredientList(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='ingredients',
    )
    measurement_unit = models.ForeignKey(
        to=Measure,
        on_delete=models.CASCADE,
        verbose_name='measurement unit',
        related_name='ingredient_list',
    )


class Ingredient(models.Model):
    ingredient = models.ForeignKey(
        to=IngredientList,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='ingredients',
    )
    amount = models.PositiveIntegerField(
        verbose_name='amount',
    )


class Tag(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='tags',
        unique=True,
    )
    color = models.CharField(
        max_length=16,
        verbose_name='Hex codes',
        unique=True
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='slugs'
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
