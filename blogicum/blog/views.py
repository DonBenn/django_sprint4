from django.views.generic import (  # type: ignore
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.http import Http404  # type: ignore
from django.urls import reverse  # type: ignore
from django.shortcuts import render, get_object_or_404, redirect  # type:ignore
from django.contrib.auth.models import User  # type: ignore
from django.core.paginator import Paginator  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.contrib.auth.mixins import (LoginRequiredMixin)  # type: ignore
from django.core.exceptions import PermissionDenied  # type: ignore
from django.utils import timezone  # type: ignore

from blog.models import Post, Category, Comment
from blog.constants import MAX_POSTS_ON_PAGE  # type: ignore
from blog.forms import PostForm, UserForm, CommentForm
from blog.mixins import OnlyAuthorMixin, PostMixin, PostFormMixin, CommentMixin


def pagination(request, queryset, max_posts_on_page):
    paginator = Paginator(queryset, max_posts_on_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


class PostCreateView(LoginRequiredMixin, PostMixin, PostFormMixin, CreateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class PostListView(PostMixin, ListView):

    queryset = Post.selection.filtering_ordering()
    ordering = '-pub_date'
    paginate_by = MAX_POSTS_ON_PAGE
    template_name = 'blog/index.html'


class PostUpdateView(OnlyAuthorMixin, PostMixin, PostFormMixin, UpdateView):

    pk_url_kwarg = 'post_id'

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if not object.is_published and object.author != self.request.user:
            return redirect('blog:post_detail', post_id=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.object.pk})


class PostDetailView(PostMixin, DetailView):
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if (not object.is_published or object.pub_date > timezone.now()) and (
                object.author != self.request.user):
            raise Http404('Пост недоступен')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


def profile(request, username):

    user = get_object_or_404(User, username=username)
    post_list = user.posts(manager='selection').profile_ordering()
    page_obj = pagination(request, post_list, MAX_POSTS_ON_PAGE)
    context = {'page_obj': page_obj,
               'profile': user}
    return render(request, 'blog/profile.html', context)


@login_required
def create_post(request, post_id=None):
    if post_id is not None:
        instance = get_object_or_404(Post, pk=post_id)
    else:
        instance = None
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=instance,
    )
    context = {'form': form}
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
    return render(request, 'blog/create.html', context)


@login_required
def delete_post(request, post_id):
    instance = get_object_or_404(Post, pk=post_id)
    if instance.author != request.user:
        raise PermissionDenied
    form = PostForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:index')
    return render(request, 'blog/create.html', context)


class CommentCreateView(LoginRequiredMixin, CreateView):
    post_obj = None
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_obj
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.post_obj.id})


class CommentDeleteView(CommentMixin, DeleteView):
    pass


class CommentUpdateView(CommentMixin, UpdateView):
    pass


def category_posts(request, category_slug):

    template = 'blog/category.html'

    category = get_object_or_404(
        Category, slug=category_slug, is_published=True)
    post_detail = Post.selection.filtered_by_category(category)
    page_obj = pagination(request, post_detail, MAX_POSTS_ON_PAGE)

    context = {'page_obj': page_obj,
               'category': category}

    return render(request, template, context)
