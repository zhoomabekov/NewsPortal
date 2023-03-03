from django import forms
from django.core.exceptions import ValidationError

from .models import Post

class PostForm(forms.ModelForm):
    author_user_username = forms.TextInput()
    title = forms.CharField(max_length=50)
    post_body = forms.CharField(min_length=20, widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))
    # добавил widget для расширения поля для ввода текста

    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'title',
            'post_body'
        ]


