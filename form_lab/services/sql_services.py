from __future__ import annotations

from typing import List, Tuple

from django.db import connection, transaction

from ..models import Author, SimpleArticle
from ..types import ArticleInput
from ..schemas import ArticleSchema


def create_article(*, data: ArticleInput) -> SimpleArticle:
    """
    SQLで記事を作成するService関数
    """
    validated = ArticleSchema(**data)

    body_length: int = len(validated.body)

    with transaction.atomic():
        author, _created = Author.objects.get_or_create(name=validated.author_name)

        with connection.cursor() as cursor:
            sql = """
            INSERT INTO form_lab_simplearticle (title, body, author_id, body_length)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """
            cursor.execute(
                sql,
                [validated.title, validated.body, author.id, body_length],
            )

            row: tuple[int] | None = cursor.fetchone()

        if row is None:
            raise RuntimeError("Failed to insert article")

        article_id: int = row[0]

        article: SimpleArticle = SimpleArticle.objects.get(id=article_id)

    return article


def list_articles() -> List[Tuple[int, str, str]]:
    """
    記事一覧を取得する（SELECT）
    """

    sql = """
    SELECT id, title, body
    FROM form_lab_simplearticle
    ORDER BY id DESC
    """

    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows: List[tuple[int, str, str]] = cursor.fetchall()

    return rows


def update_article(*, article_id: int, data: ArticleInput) -> SimpleArticle:
    """
    記事を更新する (SQL UPDATE)
    """

    validated = ArticleSchema(**data)

    body_length: int = len(validated.body)

    with transaction.atomic():
        author, _created = Author.objects.get_or_create(name=validated.author_name)

        sql = """
        UPDATE form_lab_simplearticle
        SET title = %s, body = %s, author_id = %s, body_length = %s
        WHERE id = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(
                sql,
                [
                    validated.title,
                    validated.body,
                    author.id,
                    body_length,
                    article_id,
                ],
            )

        article: SimpleArticle = SimpleArticle.objects.get(id=article_id)

    return article


def delete_article(*, article_id: int) -> None:
    """
    記事を削除する (SQL DELETE)
    """

    with transaction.atomic():
        sql = """
        DELETE FROM form_lab_simplearticle
        WHERE id = %s
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [article_id])


def get_article_stats() -> Tuple[int, int, float]:
    """
    記事の集計を取得する
    (COUNT, SUM, AVG)
    """

    sql = """
    SELECT
        COUNT(sa.id) AS article_count,
        SUM(sa.body_length) AS total_length,
        AVG(sa.body_length) AS avg_length
    FROM form_lab_simplearticle AS sa
    """

    with connection.cursor() as cursor:
        cursor.execute(sql)
        row: tuple[int, int, float] | None = cursor.fetchone()

    if row is None:
        raise RuntimeError("Failed to fetch stats")

    return row
