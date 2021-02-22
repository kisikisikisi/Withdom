from django.urls import path
from . import views



app_name = 'posts'

urlpatterns = [
    path('', views.index, name='index'),
    path('get_posts_count/<str:username>/', views.get_posts_count, name='get_posts_count'),
    path('posts/<int:post_id>/', views.post_detail, name="post_detail"),
    path('add/', views.add, name='add'),
    path('edit/<int:post_id>/', views.edit, name='edit'),
    path('delete/<int:post_id>/', views.delete, name='delete'),
    path('posts/<int:post_id>/like/', views.like, name='like'),
    path("api/like/<int:post_id>/", views.api_like, name="api_like"),
    ]