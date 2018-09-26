from .models import PostModel
from django import forms
from django.forms import ModelForm

class PostForm(forms.ModelForm):

    class Meta():
        model = PostModel
        fields = ('title','file','description')
