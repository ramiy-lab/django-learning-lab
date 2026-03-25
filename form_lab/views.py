from __future__ import annotations

from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import SimpleArticleForm
from .services import handle_article_input, ArticleInput


def article_create_view(request: HttpRequest) -> HttpResponse:
    """
    記事作成ビュー (Form → Service接続)
    """

    if request.method == "POST":
        form: SimpleArticleForm = SimpleArticleForm(data=request.POST)

        if form.is_valid():
            cleaned_data: dict[str, Any] = form.cleaned_data

            # TypedDictに詰め替え
            service_input: ArticleInput = {
                "title": cleaned_data["title"],
                "body": cleaned_data["body"],
                "author_name": cleaned_data["author_name"],
            }

            handle_article_input(data=service_input)

            return redirect("form_lab:article_create")

    else:
        form = SimpleArticleForm()

    return render(request, "form_lab/simple_article_form.html", {"form": form})
