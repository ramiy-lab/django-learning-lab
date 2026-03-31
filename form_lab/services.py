from __future__ import annotations

from pydantic import BaseModel

from django.db import connection, transaction

from .models import Author, SimpleArticle
from .types import ArticleInput


class ArticleSchema(BaseModel):
    title: str
    body: str
    author_name: str


def create_article(*, data: ArticleInput) -> SimpleArticle:
    """
    SQLで記事を作成するService関数
    """
    validated = ArticleSchema(**data)

    with transaction.atomic():
        author, _created = Author.objects.get_or_create(name=validated.author_name)

        with connection.cursor() as cursor:
            sql = """
            INSERT INTO form_lab_simplearticle (title, body, author_id)
            VALUES (%s, %s, %s)
            RETURNING id
            """
            cursor.execute(sql, [validated.title, validated.body, author.id])

            row: tuple[int] | None = cursor.fetchone()

        if row is None:
            raise RuntimeError("Failed to insert article")

        article_id: int = row[0]

        article: SimpleArticle = SimpleArticle.objects.get(id=article_id)

    return article
