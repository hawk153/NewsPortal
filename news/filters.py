from django_filters import FilterSet
from django.forms import DateInput
from django_filters import DateFilter, CharFilter, ModelChoiceFilter
from .models import Post, Category


class FilterNews(FilterSet):
    title = CharFilter(label='Заголовок содержит:', lookup_expr='icontains')
    post_category = ModelChoiceFilter(field_name='post_category',
                                      queryset=Category.objects.all(),
                                      lookup_expr='exact', label='Категория',
                                      empty_label='Любая категория')
    date_creation = DateFilter(
        field_name='post_creation_date',
        lookup_expr='gt',
        label='Дата',
        widget=DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
    )

    class Meta:
        model = Post
        # fields = {'postcategory__categories': ['exact']}
        fields = ['title', 'post_category', 'date_creation']
