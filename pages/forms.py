from __future__ import annotations

from typing import TYPE_CHECKING

from django import forms

from pages.models import Article


if TYPE_CHECKING:
    BaseArticleForm = forms.ModelForm[Article]

else:
    BaseArticleForm = forms.ModelForm


class ArticleCreateForm(BaseArticleForm):
    """
    Article作成フォーム
    """

    class Meta:
        model = Article

        fields = [
            "title",
            "body",
        ]


class ContactForm(forms.Form):
    """
    簡易お問い合わせフォーム
    """

    name: forms.CharField = forms.CharField(
        max_length=100,
        label="Name",
    )

    email: forms.EmailField = forms.EmailField(
        label="Email",
    )

    message: forms.CharField = forms.CharField(
        widget=forms.Textarea,
        label="Message",
    )
