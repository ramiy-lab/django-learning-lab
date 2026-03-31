from __future__ import annotations

from typing import cast

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import SimpleArticleForm
from .services import create_article
from .types import ArticleInput


def article_create_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SimpleArticleForm(request.POST)

        if form.is_valid():
            cleaned_data = cast(ArticleInput, form.cleaned_data)
            service_input: ArticleInput = {
                "title": cleaned_data["title"],
                "body": cleaned_data["body"],
                "author_name": cleaned_data["author_name"],
            }

            create_article(data=service_input)

            return redirect("form_lab:article_create")

    else:
        form = SimpleArticleForm()

    return render(request, "form_lab/simple_article_form.html", {"form": form})
