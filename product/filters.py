from django_filters import rest_framework as filters
from .models import Product


class ProductsFilter(filters.FilterSet):
    keyword = filters.CharFilter(field_name="name",lookup_expr="icontains")
    max_price = filters.NumberFilter(field_name="price" or 1000000,lookup_expr="lte")
    min_price = filters.NumberFilter(field_name="price" or 0,lookup_expr="gte")

    class Meta:
        model = Product
        fields = ('category','brand','keyword','max_price','min_price')