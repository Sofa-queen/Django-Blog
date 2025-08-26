from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from blog.constants import POSTS_AMOUNT
from blog.models import Category, Post, Comment, CommentForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator


def index(request):
    template = 'blog/index.html'
    posts_list = Post.filter_manager.all()
    paginator = Paginator(posts_list, POSTS_AMOUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post.filter_manager.all(), pk=post_id)
    form = CommentForm(request.POST or None)
    comments = Comment.objects.filter(post=post).select_related('author').order_by('-created_at')
    context = {'post': post,
               'form': form,
               'comments': comments
               }
    template = 'blog/detail.html'
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = category.post_category.published()
    paginator = Paginator(post_list, POSTS_AMOUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category,
               'page_obj': page_obj}
    return render(request, template, context)


def profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    posts_list = Post.objects.filter(author=user_obj).order_by('-created_at')

    paginator = Paginator(posts_list, POSTS_AMOUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': user_obj,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('login'))
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration_form.html', {'form': form})


class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user.username})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = ['username', 'first_name', 'last_name']

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user.username})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create.html'
    fields = ['title', 'text', 'category', 'location', 'pub_date', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        username = self.request.user.username
        return reverse('blog:profile', kwargs={'username': username})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    fields = ['title', 'text', 'category', 'location', 'pub_date', 'image']

    def get_object(self, queryset=None):
        post_id = self.kwargs.get('pk')
        return get_object_or_404(Post, pk=post_id)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        return redirect('post_detail', pk=self.get_object().pk)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.object.pk})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['post_id']
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.kwargs['post_id']})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def get_queryset(self):
        # Разрешить редактировать только свои комментарии
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.object.post_id})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_object(self):
        comment_id = self.kwargs.get('pk')
        return get_object_or_404(Comment, pk=comment_id)

    def get_success_url(self):
        post_id = self.object.post.id
        return reverse_lazy('blog:post_detail', kwargs={'post_id': post_id})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user.username})


def trigger_error(request):
    1 / 0  # делим на ноль, вызовет ZeroDivisionError
    return HttpResponse("Никогда не дойдёт сюда :)")
