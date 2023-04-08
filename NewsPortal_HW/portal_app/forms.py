from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    # author = forms.ModelChoiceField(queryset=Author.objects.all(), label='Author name',
    #                                 empty_label=None, to_field_name='user')
    # The above code is needed since the author will be automatically recorded

    title = forms.CharField(max_length=50)
    post_body = forms.CharField(min_length=20, widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))
    # добавил widget для расширения поля для ввода текста

    class Meta:
        model = Post
        fields = [
            'categories',
            'title',
            'post_body'
        ]
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)                    #переопределяем init для того, чтобы использовать названия Категорий
        self.fields['categories'].label_from_instance = lambda obj: obj.name

