from django_filters import CharFilter, DateFilter, FilterSet
from .models import Student


class StudentFilter(FilterSet):
    start_date = DateFilter(field_name='birth_date', lookup_expr='gte')
    end_date = DateFilter(field_name='birth_date', lookup_expr='lte')
    last_name = CharFilter(field_name='last_name', lookup_expr='contains', label='Фамилия')
    first_name = CharFilter(field_name='first_name', lookup_expr='contains', label='Имя')

    class Meta:
        model = Student
        fields = ['last_name', 'first_name', 'group']