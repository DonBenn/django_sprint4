from django import forms  # type: ignore
from django.contrib.auth.models import User  # type: ignore

from blog.models import Post, Comments


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'}),
            'text': forms.Textarea(attrs={'class': 'form-control'})}


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('text',)
