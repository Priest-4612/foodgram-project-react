import django_filters as filters

from recipes.models import Ingredient, Recipe, Tag  # isort:skip


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(
        to_field_name='slug',
        field_name='tags__slug',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags']


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', method='starts_with')

    class Meta:
        model = Ingredient
        fields = ['name']

    def starts_with(self, queryset, slug, name):
        return queryset.filter(name__startswith=name)
