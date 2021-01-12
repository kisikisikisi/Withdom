from django.db import models
from mdeditor.fields import MDTextField
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    published = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='media/')
    body = MDTextField()

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:120]