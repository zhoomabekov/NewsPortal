from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.template import context
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, CategorySubscriber, Subscriber
from .filters import PostFilter
from .forms import PostForm
from .tasks import new_post_notification, hello


class PostsList(PermissionRequiredMixin, ListView):
    permission_required = ('portal_app.view_post')
    model = Post
    ordering = '-post_created'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['categories'] = Category.objects.all()
        return context


class PostsSearch(PermissionRequiredMixin, ListView):
    permission_required = ('portal_app.view_post')
    model = Post
    ordering = '-post_created'
    template_name = 'posts_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(PermissionRequiredMixin, DetailView):
    permission_required = ('portal_app.view_post')
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('portal_app.add_post')

    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user.author
        if 'article' in self.request.path:
            post.type = 'a'
        elif 'news' in self.request.path:
            post.type = 'n'
        post.save()
        form.save_m2m()  # saving many-to-many relationships if any
        new_post_notification.delay(post.id)
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('portal_app.change_post')
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('portal_app.delete_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')


class PostsListInCategory(PostsList):
    template_name = 'posts_in_category.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            queryset = queryset.filter(categories=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        context['category'] = category
        return context


class SubscribeCategoryView(View):
    def post(self, request, *args, **kwargs):
        category_id = self.kwargs['category_id']
        category = Category.objects.get(pk=category_id)

        subscriber = request.user.subscriber
        subscription, created = CategorySubscriber.objects.get_or_create(category=category, subscriber=subscriber)
        # If the subscription already exists, display a warning message
        if not created:
            messages.warning(request, 'You are already subscribed to this category.')
            return redirect('posts_in_category', category_id=category.id)

        # If the subscription is new, display a success message
        messages.success(request, 'You have successfully subscribed to this category.')

        return redirect('posts_in_category', category_id=category.id)


def login_view(request):
    if request.method == 'POST':
        # ...authenticate user...
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        subscriber = Subscriber.objects.create(user=user)
        print(subscriber)
        if user is not None:
            login(request, user)
            # Create a new Subscriber object for the user

            # redirect to the home page
            return redirect('home')
    else:
        # ...render login form...
        return render(request, 'login.html', context)
