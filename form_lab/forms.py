from django import forms
from .models import SimpleArticle


class SimpleArticleForm(forms.ModelForm):
    class Meta:
        model = SimpleArticle
        fields = ["title", "body"]
