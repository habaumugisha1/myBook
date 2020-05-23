import django_filters
from django_filters import DateFilter, CharFilter
from .models import *
from account.models import FinalProjects


class PostFilter(django_filters.FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')
    start_date = DateFilter(field_name="date_posted", lookup_expr='gte')

    class Meta:
        model = FinalProjects
        exclude = ['content', 'date_posted', 'introduction', 'problem_statement', 'scope', 'source_code', 'author']
        fields = '__all__'
