from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from .models import Post
from .models import Comment
from django.urls import reverse_lazy
from .forms import PostAddForm
from django.http.response import JsonResponse
from django.db.models import Q, Sum
from django.contrib import messages
from functools import reduce
from operator import and_
from taggit.models import Tag


def search_keyword(keyword, posts):
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
    return posts

def index(request):
    posts = Post.objects.order_by('-published')
    posts_filter = Post.objects.filter(author=request.user.id)
    posts_like = posts_filter.aggregate(Sum('like'))
    posts_views = posts_filter.aggregate(Sum('views'))
    keyword = request.GET.get('keyword')
    if keyword:
        posts = search_keyword(keyword, posts)
        messages.success(request, '「{}」の検索結果'.format(keyword))
        return render(request, 'posts/index.html', {'posts': posts, 'posts_count': len(posts_filter), 'posts_filter': posts_filter, 'posts_like': posts_like['like__sum'], 'posts_views': posts_views['views__sum']})
    else:
        return render(request, 'posts/index.html', {'posts': posts, 'posts_count': len(posts_filter), 'posts_filter': posts_filter, 'posts_like': posts_like['like__sum'], 'posts_views': posts_views['views__sum']})


def about(request):
    return render(request, 'posts/about.html')


def top(request):
    posts = Post.objects.order_by('-published')
    posts_filter = Post.objects.filter(author=request.user.id)
    posts_like = posts_filter.aggregate(Sum('like'))
    posts_views = posts_filter.aggregate(Sum('views'))
    keyword = request.GET.get('keyword')
    if keyword:
        posts = search_keyword(keyword, posts)
        messages.success(request, '「{}」の検索結果'.format(keyword))
        return render(request, 'posts/index.html', {'posts': posts})
    else:
        return render(request, 'posts/top.html', {'posts': posts, 'posts_count': len(posts_filter), 'posts_filter': posts_filter, 'posts_like': posts_like['like__sum'], 'posts_views': posts_views['views__sum']})

def get_posts_count(request, username):
    posts = Post.objects.filter(author=request.user.id)
    return JsonResponse({'posts_count': len(posts)})
    

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.views += 1
    post.save()
    keyword = request.GET.get('keyword')
    if keyword:
        posts = search_keyword(keyword, Post.objects.order_by('-published'))
        messages.success(request, '「{}」の検索結果'.format(keyword))
        return render(request, 'posts/index.html', {'posts': posts})
    else:
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
    posts_filter = Post.objects.filter(author=request.user.id)
    posts_like = posts_filter.aggregate(Sum('like'))
    posts_views = posts_filter.aggregate(Sum('views'))
    keyword = request.GET.get('keyword')
    if keyword:
        posts = search_keyword(keyword, posts)
        messages.success(request, '「{}」の検索結果'.format(keyword))
        return render(request, 'posts/index.html', {'posts': posts, 'posts_count': len(posts_filter), 'posts_filter': posts_filter, 'posts_like': posts_like['like__sum'], 'posts_views': posts_views['views__sum']})
    else:
        return render(request, 'posts/index.html', {'posts': posts, 'posts_count': len(posts_filter), 'posts_filter': posts_filter, 'posts_like': posts_like['like__sum'], 'posts_views': posts_views['views__sum']})
