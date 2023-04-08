from django.db import models
from django.contrib.auth.models import User
from django.db.models import ForeignKey
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).values('post_rating')
        posts_rating_sum_3 =sum([rate['post_rating'] for rate in posts_rating])*3

        author_comments_rating = Comment.objects.filter(commenter=self.user).values('comment_rating')
        author_comments_rating_sum = sum([rate['comment_rating'] for rate in author_comments_rating])

        posts_comments_rating = Post.objects.filter(author=self).values('comments__comment_rating')
        posts_comments_rating_sum = 0
        for i in posts_comments_rating:
            vals = i['comments__comment_rating']
            if vals:
                posts_comments_rating_sum += vals

        self.author_rating = posts_rating_sum_3 + author_comments_rating_sum + posts_comments_rating_sum
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    subscribers = models.ManyToManyField('Subscriber', through='CategorySubscriber', related_name='subscribed_categories')

class Subscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

class CategorySubscriber(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)


class Post(models.Model):
    post_news = [('a', 'article'), ('n', 'news')]

    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='posts')
    type = models.CharField(max_length=1, choices=post_news, default='a')
    post_created = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', through='PostCategory', related_name='posts')
    title = models.CharField(max_length=50, unique=True)
    post_body = models.TextField()
    post_rating = models.IntegerField(default=0)
    _preview = models.CharField(max_length=200, null=True, db_column='preview')

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    @property
    def preview(self):
        return self._preview

    @preview.setter
    def preview(self):
        self._preview = self.post_body[:123] + '...'
        return self._preview
        self.save()

    def __str__(self):
        return f'{self.title}: {self.post_body[:20]}...'

    # Подсказать Django, какую страницу нужно открыть после создания инстанса через форму.
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment_body = models.TextField()
    comment_created = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

