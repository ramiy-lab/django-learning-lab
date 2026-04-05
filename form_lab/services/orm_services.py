from typing import List, Tuple

from pydantic import BaseModel

from django.db import transaction

from .models import Author, SimpleArticle
from .types import ArticleInput


class ArticleSchema(BaseModel):
    title: str
    body: str
    author_name: str


def create_article(*, data: ArticleInput) -> SimpleArticle:
    """
    ORMで記事を作成するService関数
    """
    validated = ArticleSchema(**data)

    with transaction.atomic():
        author, _created = Author.objects.get_or_create(
            name=validated.author_name
        )

        article: SimpleArticle = SimpleArticle.objects.create(
            title=validated.title,
            body=validated.body,
            author=author,
        )

    return article


def list_articles() -> List[Tuple[int, str, str]]:
    """
    記事一覧を取得する (ORM SELECT)
    """

    articles = SimpleArticle.objects.all().order_by("-id")

    rows: List[Tuple[int, str, str]] = [
        (article.id, article.title, article.body)
        for article in articles
    ]

    return rows


def update_article(*, article_id: int, data: ArticleInput) -> SimpleArticle:
    """
    記事を更新する (ORM UPDATE)
    """

    validated = ArticleSchema(**data)

    with transaction.atomic():
        article: SimpleArticle = SimpleArticle.objects.get(id=article_id)

        author, _created = Author.objects.get_or_created(
            name=validated.author_name
        )

        article.title = validated.title
        article.body = validated.body
        article.author = author

        article.save()

    return article


def delete_article(*, article_id: int) -> None:
    """
    記事を削除する (ORM DELETE)
    """

    with transaction.atomic():
        article: SimpleArticle = SimpleArticle.object.get(id=article_id)
        article.delete()
