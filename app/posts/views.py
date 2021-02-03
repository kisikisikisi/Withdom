from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from .models import Post
from .models import Comment
from django.urls import reverse_lazy
from .forms import PostAddForm
from django.http.response import JsonResponse
from django.db.models import Q
from django.contrib import messages
from functools import reduce
from operator import and_
from taggit.models import Tag


def index(request):
    posts = Post.objects.order_by('-published')
    return render(request, 'posts/index.html', {'posts': posts})


def about(request):
    return render(request, 'posts/about.html')

def top(request):
    posts = Post.objects.order_by('-published')
    keyword = request.GET.get('keyword')
    if keyword:
        exclusion_list = set([' ', '　'])
        q_list = ''
        for word in keyword:
            if word in exclusion_list:
                pass
            else:
                q_list += word

        query = reduce(
                    and_, [Q(title__icontains=q) | Q(body__icontains=q)
                             for q in q_list]
                )
        posts = posts.filter(query)
        messages.success(request, '「{}」の検索結果'.format(keyword))
        return render(request, 'posts/index.html', {'posts': posts})
    else:
        return render(request, 'posts/top.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.views += 1
    post.save()
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
            form.save_m2m()
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
    return JsonResponse({"like": post.like})


def categol_list(request, categol):
    posts = Post.objects.filter(tags__name__in=[categol])
    return render(request, 'posts/index.html', {'posts': posts})


