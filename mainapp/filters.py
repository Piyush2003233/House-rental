import django_filters
from django_filters import RangeFilter
from .models import ListingModel


class FilterDemo(django_filters.FilterSet):
    price = RangeFilter()

    class Meta:
        model = ListingModel
        fields = ['apartment_type', 'price']
