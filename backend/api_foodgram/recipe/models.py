from django.db import models


class Measure(models.Model):
    name = models.CharField(
        max_length=32,
        verbose_name = 'measure',
        unique=True,
    )


class Ingredient(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='ingredients',
        unique=True,
    )
    measurement_unit = models.ForeignKey(
        to=Measure,
        on_delete=models.SET_NULL,
        related_name='measures',
        verbose_name='measurement unit',
        unique=True,
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
    # author
    name = models.CharField(
        max_length=256,
        verbose_name='recipes'
    )
    image = models.ImageField(
        upload_to='recipies/',
    )
    description = models.TextField()
    # ingredients
    # tags
    cooking_time = models.IntegerField()
