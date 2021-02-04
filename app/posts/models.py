from django.db import models
from mdeditor.fields import MDTextField
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from taggit.models import Tag
from markdown import markdown

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    tags = TaggableManager(blank=True)
    published = models.DateTimeField(default=timezone.now, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    image = models.ImageField(upload_to='media/', blank=True)
    body = MDTextField()
    like = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:120]

    def get_tags(self):
        tags = list(Tag.objects.all())
        menu = {}
        for tag in tags:
            count = len(Post.objects.filter(tags__name__in=[tag]))
            if count > 0:
                menu[str(tag)] = count
        menu_sorted = sorted(menu.items(), key=lambda x:x[1], reverse=True)
        return dict(menu_sorted)

    def sort_like(self):
        posts = Post.objects.order_by('-like')
        return posts

    def sort_views(self):
        posts = Post.objects.order_by('-views')
        return posts
    
    def get_posts_count(self, username):
        posts = Post.objects.filter(author=username)
        print(len(posts))


class Comment(models.Model):
    text = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.text
