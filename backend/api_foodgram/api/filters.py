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
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ["author__id", "tags__slug",
                  "is_favorited", "is_in_shopping_cart"]

    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(is_favorited__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(
                is_in_shopping_cart__user=self.request.user
            )
        return queryset


class IngredientFilter(SearchFilter):
    search_param = 'name'
