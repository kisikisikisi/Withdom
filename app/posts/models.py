from django.db import models
from mdeditor.fields import MDTextField
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    published = models.DateTimeField(default=timezone.now, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    image = models.ImageField(upload_to='media/', blank=True)
    body = MDTextField()

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:120]