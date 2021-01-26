"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from posts import views
from django.views.generic import base

urlpatterns = [
    path('posts/', include('posts.urls')),
    path('', views.top, name='top'),
    path('about/', views.about, name='about'),
    path("api/like/<int:post_id>/", views.api_like, name="api_like"),
    path('admin/', admin.site.urls),
    path('categol_list/<str:categol>/', views.categol_list, name='categol_list'),
    path('posts/<int:post_id>/', views.post_detail, name="post_detail"),
    path('posts/<int:post_id>/like/', views.like, name='like'),
    path('accounts/', include('accounts.urls')),
    path('accounts/profile/', base.RedirectView.as_view(url="/")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
