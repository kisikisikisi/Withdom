from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from .models import Post
from .models import Comment
from django.urls import reverse_lazy
from .forms import PostAddForm
from django.http.response import JsonResponse


def index(request):
    posts = Post.objects.order_by('-published')
    return render(request, 'posts/index.html', {'posts': posts})

def top(request):
    posts = Post.objects.order_by('-published')
    return render(request, 'posts/top.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        Comment.objects.create(text=request.POST["text"], article=post)
    return render(request, 'posts/post_detail.html', {'post': post})


def add(request):
    if request.method == "POST":
        form = PostAddForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:index')
    else:
        form = PostAddForm()
    return render(request, 'posts/add.html', {'form': form})


def edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = PostAddForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post.author = request.user
            form.save()
            return redirect('posts:post_detail', post_id=post.id)
    else:
        form = PostAddForm(instance=post)
    return render(request, 'posts/edit.html', {'form': form, 'post': post})


def delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
    return redirect('posts:index')


def like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.like += 1
    post.save()
    return redirect('posts:post_detail', post_id)

def api_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.like += 1
    post.save() 
    return JsonResponse({"like":post.like})
