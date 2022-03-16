from django_filters import rest_framework as filters
from django_filters import widgets
from rest_framework.filters import SearchFilter

from recipes.models import Recipe  # isort:skip


class RecipeFilter(filters.FilterSet):
    author = filters.AllValuesMultipleFilter(
        field_name='author__id'
    )
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        widget=widgets.BooleanWidget()
    )

    class Meta:
        model = Recipe
        fields = ["author__id", "tags__slug",
                  "is_favorited", "is_in_shopping_cart"]


class IngredientFilter(SearchFilter):
    search_param = 'name'
