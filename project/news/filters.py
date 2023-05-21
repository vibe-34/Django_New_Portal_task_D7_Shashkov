from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter
from django.forms import DateInput
from .models import Category


class RecordFilter(FilterSet):

    category = ModelChoiceFilter(field_name='category__title',
                                 queryset=Category.objects.all(),
                                 label='Категория',
                                 empty_label='Категория не выбрана')

    title = CharFilter(lookup_expr='contains',)

    date = DateFilter(field_name='data', lookup_expr='gt', label='Дата', widget=DateInput(attrs={'type': 'date'},))
