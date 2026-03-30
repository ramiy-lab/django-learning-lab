from __future__ import annotations

from typing import Any, cast

from django import forms


class SimpleArticleForm(forms.Form):
    title: forms.CharField = forms.CharField(
        max_length=100,
        label="Title",
    )
    body: forms.CharField = forms.CharField(
        widget=forms.Textarea,
        label="Body",
    )
    author_name: forms.CharField = forms.CharField(
        max_length=100,
        label="Author Name",
    )

    def clean_title(self) -> str:
        """
        フィールド単位バリデーション
        """
        title: str = self.cleaned_data["title"]

        if "禁止" in title:
            raise forms.ValidationError("タイトルに禁止ワードが含まれています")

        return title

    def clean(self) -> dict[str, Any]:
        """
        全体バリデーション
        """
        cleaned_data = cast(dict[str, Any], super().clean())

        title: str = cleaned_data.get("title", "")
        body: str = cleaned_data.get("body", "")

        if title and body and title == body:
            raise forms.ValidationError("タイトルと本文が同じ内容です")

        return cleaned_data
