from django.urls import path
from .views import PostsList, PostsSearch, PostDetail, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    path('posts/', PostsList.as_view(), name='posts_list'),
    path('posts/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('posts/search/', PostsSearch.as_view(), name='posts_search_list'),

    path('articles/create/', PostCreate.as_view(), name='article_create'),
    path('article/<int:pk>/update/', PostUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),

    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),

]