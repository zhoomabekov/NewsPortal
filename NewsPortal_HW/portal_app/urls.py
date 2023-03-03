from django.urls import path
from .views import PostsList, PostDetail, ArticleCreate

urlpatterns = [
    path('news/', PostsList.as_view(), name='post_list'),
    path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    # path('posts/create/', ArticleCreate.as_view(), name='post_create'),
    # path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    # path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]