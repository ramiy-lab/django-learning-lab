from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from django import forms

from .models import Author, SimpleArticle


if TYPE_CHECKING:
    BaseArticleForm = forms.ModelForm[SimpleArticle]
else:
    BaseArticleForm = forms.ModelForm


class SimpleArticleForm(BaseArticleForm):
    author_name: forms.CharField = forms.CharField(
        max_length=100,
        label="Author Name",
        help_text="著者名を入力してください",
    )

    class Meta:
        model = SimpleArticle
        fields = ["title", "body", "author_name"]

    def clean_title(self) -> str:
        title: str = self.cleaned_data["title"]

        if len(title) < 3:
            raise forms.ValidationError("タイトルは3文字以上にしてください")

        if "spam" in title.lower():
            raise forms.ValidationError("タイトルに禁止ワードが含まれています")

        return title

    def clean_author_name(self) -> str:
        name: str = self.cleaned_data["author_name"]

        normalized: str = name.strip()
        if not normalized:
            raise forms.ValidationError("Author Name は空白だけでは登録できません")

        return normalized

    def clean(self) -> dict[str, Any]:
        """
        フォーム全体のバリデーション

        ルール:
        ・title に "draft" が含まれる場合
         → body は必須
        """
        cleaned_data = cast(dict[str, Any], super().clean())

        title: str | None = cleaned_data.get("title")
        body: str | None = cleaned_data.get("body")

        if title is None:
            return cleaned_data

        if "draft" in title.lower():
            if not body:
                self.add_error("body", "draft記事の場合、本文は必須です")

        return cleaned_data

    def save(self, commit: bool = True) -> SimpleArticle:
        article: SimpleArticle = super().save(commit=False)

        author_name: str = self.cleaned_data["author_name"]
        author, _created = Author.objects.get_or_create(name=author_name)

        article.author = author

        if commit:
            article.save()

        return article
