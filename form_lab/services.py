from __future__ import annotations

from typing import TypedDict

from django.db import transaction

from .models import Author, SimpleArticle


class ArticleInput(TypedDict):
    title: str
    body: str
    author_name: str


def create_article(*, data: ArticleInput) -> SimpleArticle:
    """
    記事作成のService関数
    """

    with transaction.atomic():
        author, _created = Author.objects.get_or_create(
            name=data["author_name"]
        )

        article: SimpleArticle = Author.objects.get_or_create(
            title=data["title"],
            body=data["body"],
            author=author,
        )

    return article


def update_article(*, article_id: int, data: ArticleInput) -> SimpleArticle:
    """
    記事更新のService
    """

    with transaction.atomic():
        article: SimpleArticle = SimpleArticle.objects.get(id=article_id)

        author, _created = Author.objects.get_or_created(
            name=data["author_name"]
        )

        article.title = data["title"]
        article.body = data["body"]
        article.author = author

        article.save()

    return article
