from __future__ import annotations

from typing import TYPE_CHECKING

from django import forms
from django.db import transaction

from .models import Author, SimpleArticle


if TYPE_CHECKING:
    BaseArticleForm = forms.ModelForm[SimpleArticle]
else:
    BaseArticleForm = forms.ModelForm


class SimpleArticleForm(BaseArticleForm):
    author_name: forms.Charfield = forms.CharField(
        max_length=100,
        label="Author Name",
    )

    class Meta:
        model = SimpleArticle
        fields = ["title", "body", "author_name"]

    def save(self, commit: bool = True) -> SimpleArticle:
        article: SimpleArticle = super().save(commit=False)
        author_name: str = self.cleaned_data["author_name"]

        with transaction.atomic():
            author, _created = Author.objects.get_or_create(name=author_name)
            article.author = author
            if commit:
                article.save()

        return article
