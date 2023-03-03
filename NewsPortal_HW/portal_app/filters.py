import django_filters
from django.forms import DateInput
from django_filters import FilterSet, DateFilter, CharFilter
from .models import Post

class PostFilter(FilterSet):
    author__user__username  = CharFilter(lookup_expr='icontains', label='Author name')
    post_created = DateFilter(field_name='post_created', lookup_expr='gt', label="Posts after the date",
                              widget=DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
        }
