from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, IngredientList, Measure,
                     Recipe, Tag)


@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']
    list_display_links = ['name']
    search_fields = ['name']


@admin.register(IngredientList)
class IngredientListAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'measurement_unit']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['name']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['pk', 'ingredient', 'amount']
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
    list_display = ['author', 'name', 'image', 'description',
                    'cooking_time']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['name', 'author', 'tags']


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'author']
    search_fields = ['user', 'author']
    list_filter = ['user', 'author']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'recipe']
    search_fields = ['user', 'recipe']
    list_filter = ['user', 'recipe']
