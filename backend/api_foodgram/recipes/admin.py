from django.contrib import admin

from .models import (Favorite, Ingredient, Measure, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    list_display_links = ['name']
    search_fields = ['name']


@admin.register(Ingredient)
class IngredientListAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'measurement_unit']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['name']


@admin.register(RecipeIngredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['pk', 'recipe', 'ingredient', 'amount']
    list_display_links = ['ingredient']
    search_fields = ['ingredient']
    list_filter = ['ingredient']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'color', 'slug']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['name']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['author', 'name', 'image', 'text',
                    'cooking_time']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['name', 'author', 'tags']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'recipe']
    search_fields = ['user', 'recipe']
    list_filter = ['user', 'recipe']


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'recipe']
    search_fields = ['user', 'recipe']
    list_filter = ['user', 'recipe']
