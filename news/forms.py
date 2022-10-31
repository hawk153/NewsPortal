
from django import forms
from django.forms import ChoiceField

from .models import Post
from django_filters import ModelChoiceFilter
from .models import Category


class CreateForm(forms.ModelForm):
    title = forms.CharField(min_length=10, max_length=100, label='Заголовок')
    post_content = forms.CharField(widget=forms.Textarea({'rows': '5'}), label='Содержимое', min_length=200)

    class Meta:
        model = Post
        fields = ['post_type',
                  'author_name',
                  'post_category',
                  'title',
                  'post_content',
                  ]