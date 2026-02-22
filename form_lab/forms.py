from django import forms
from .models import SimpleArticle


class SimpleArticleForm(forms.ModelForm[SimpleArticle]):
    class Meta:
        model = SimpleArticle
        fields = ["title", "body", "author"]
