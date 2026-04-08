from __future__ import annotations

from typing import cast

from django.http import HttpRequest, HttpResponse
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .models import SimpleArticle
from .forms import SimpleArticleForm
from .services import (
    create_article,
    list_articles,
    update_article,
    delete_article,
    fetch_articles_with_authors,
    fetch_articles_with_authors_left,
)
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


def article_list_plain_view(request: HttpRequest) -> HttpResponse:
    articles = list_articles()

    print("DEBUG:", articles)

    return render(
        request,
        "form_lab/article_list.html",
        {
            "articles": articles,
            "mode": "plain",
        },
    )


def article_list_with_author_view(request: HttpRequest) -> HttpResponse:
    articles = fetch_articles_with_authors()
    return render(
        request,
        "form_lab/article_list.html",
        {
            "articles": articles,
            "mode": "with_author",
        },
    )


def article_list_with_author_left_view(request: HttpRequest) -> HttpResponse:
    articles = fetch_articles_with_authors_left()
    return render(
        request,
        "form_lab/article_list.html",
        {
            "articles": articles,
            "mode": "with_author_left",
        },
    )


def article_update_view(request: HttpRequest, article_id: int) -> HttpResponse:

    article = get_object_or_404(SimpleArticle, id=article_id)

    if request.method == "POST":
        form = SimpleArticleForm(request.POST)

        if form.is_valid():
            cleaned_data = cast(ArticleInput, form.cleaned_data)

            service_input: ArticleInput = {
                "title": cleaned_data["title"],
                "body": cleaned_data["body"],
                "author_name": cleaned_data["author_name"],
            }

            update_article(article_id=article_id, data=service_input)

            return redirect("form_lab:article_list")

    else:
        form = SimpleArticleForm(
            initial={
                "title": article.title,
                "body": article.body,
                "author_name": article.author.name,
            }
        )

    return render(
        request,
        "form_lab/simple_article_form.html",
        {
            "form": form,
            "mode": "update",
        },
    )


def article_delete_view(request: HttpRequest, article_id: int) -> HttpResponse:

    if request.method == "POST":
        delete_article(article_id=article_id)

        return redirect("form_lab:article_list")

    return redirect("form_lab:article_list")
