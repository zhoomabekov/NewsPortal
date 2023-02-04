from django.db import models

class Author(models.Model):
    full_name = models.CharField(max_length=100)
    age = models.IntegerField(blank=True)
    email = models.CharField(max_length=100, blank=True)
