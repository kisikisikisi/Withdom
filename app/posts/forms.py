from django import forms
from .models import Post
from django.forms import ModelForm

class PostAddForm(forms.ModelForm):    
   class Meta:
       model = Post
       fields = ['title', 'tags', 'published', 'author', 'body', 'image']
       