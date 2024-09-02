from django.contrib.auth.mixins import (  # type: ignore
    UserPassesTestMixin)  # type: ignore
from django.views.generic import View  # type: ignore
from django.shortcuts import redirect  # type: ignore
from django.urls import reverse_lazy  # type: ignore

from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class PostMixin:
    model = Post


class PostFormMixin:
    form_class = PostForm
    template_name = 'blog/create.html'


class CommentMixin(OnlyAuthorMixin, View):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.kwargs['comment_id'])

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.kwargs['pk']},)
