from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from.models import Post
from .filters import PostFilter
from .forms import  ArticleForm

class PostsList(ListView):
    model = Post
    ordering = '-post_created'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class ArticleCreate(CreateView):
    form_class = ArticleForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        work = form.save(commit=False)
        work.type = 'n'
        return super().form_valid(form)

# # Добавляем представление для изменения товара.
# class PostUpdate(UpdateView):
#     form_class = PostForm
#     model = Post
#     template_name = 'post_edit.html'
#
# # Представление удаляющее товар.
# class PostDelete(DeleteView):
#     model = Post
#     template_name = 'post_delete.html'
#     success_url = reverse_lazy('post_list')

