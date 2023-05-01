from django.urls import path, include
from .views import PostsList, PostsSearch, PostDetail, PostCreate, PostUpdate, PostDelete, PostsListInCategory, \
    SubscribeCategoryView
from django.views.generic import RedirectView
from django.views.decorators.cache import cache_page

urlpatterns = [
    # path('', RedirectView.as_view(url='accounts/')),  # instead of error page, it will redirect to the needed page
    path('posts/', cache_page(60)(PostsList.as_view()), name='posts_list'),
    path('posts/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('posts/search/', PostsSearch.as_view(), name='posts_search_list'),

    path('article/create/', PostCreate.as_view(), name='article_create'),
    path('article/<int:pk>/update/', PostUpdate.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),

    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),

    path('category/<int:category_id>/', PostsListInCategory.as_view(), name='posts_in_category'),
    path('category/<int:category_id>/subscribe/', SubscribeCategoryView.as_view(), name='subscribe_category'),
]
