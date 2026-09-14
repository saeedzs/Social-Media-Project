from django.urls import path
from . import views

urlpatterns = [
    path('create',views.post_create,name='create'),
    path('feed',views.feed,name='feed'),
    path('like', views.like_post, name='like_post'),
    path('comment', views.feed, name='comment_post'),
    path('edit/<int:post_id>', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>', views.delete_post, name='delete_post'),

]
