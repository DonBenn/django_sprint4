from django.urls import path  # type: ignore

from blog import views


app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path(
        'posts/<int:post_id>/', views.PostDetailView.as_view(),
        name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path(
        'posts/<int:post_id>/edit/', views.PostUpdateView.as_view(),
        name='edit_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path('edit_profile/', views.UserUpdateView.as_view(), name='edit_profile'),
    path(
        'posts/<int:pk>/comment/', views.CommentsCreateView.as_view(),
        name='add_comment'),
    path(
        'posts/<int:pk>/edit_comment/<int:comment_id>/',
        views.CommentsUpdateView.as_view(), name='edit_comment'),
    path('posts/<int:pk>/delete_comment/<int:comment_id>/',
         views.CommentsDeleteView.as_view(), name='delete_comment'),
]
