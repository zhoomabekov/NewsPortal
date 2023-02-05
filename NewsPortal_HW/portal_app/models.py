from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    # def update_rating(self):
    #     posts_rating = sum(Post.objects.filter(post__author=self.user).values('self.post__post_rating')) * 3
    #     author_comments_rating = sum(
    #         Comment.objects.filter(comment__author=self.user).values('self.comment__comment_rating'))
    #     posts_comments_rating = sum(
    #         Post.objects.filter(post__author=self.user).values('self.post__comment__comment_rating'))
    #     self.author_rating = posts_rating + author_comments_rating + posts_comments_rating
    #     self.save()


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)


class Post(models.Model):
    post_news = [('p', 'post'), ('n', 'news')]

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=post_news, default='p')
    post_created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=50)
    post_body = models.TextField()
    post_rating = models.IntegerField(default=0)

    # def like(self):
    #     self.post_rating += 1
    #     self.save()
    #
    # def dislike(self):
    #     self.post_rating -= 1
    #     self.save()
    #
    # def preview(self):
    #     return self.post_body[:123] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_body = models.TextField()
    comment_created = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    # def like(self):
    #     self.comment_rating += 1
    #     self.save()
    #
    # def dislike(self):
    #     self.comment_rating -= 1
    #     self.save()
