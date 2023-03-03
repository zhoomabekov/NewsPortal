from django_filters import FilterSet, CharFilter
from .models import Post

class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author__user__username': ['icontains'],
            # 'date_later'
        }