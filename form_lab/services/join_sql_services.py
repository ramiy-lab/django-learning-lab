from __future__ import annotations

from typing import List
from django.db import connection

from ..types import ArticleAuthorRow
from ..schemas import ArticleAuthorSchema


def fetch_articles_with_authors() -> List[ArticleAuthorRow]:
    """
    ArticleとAuthorをINNER JOINして
    titleとauthor_nameを取得する
    """

    query: str = """
        SELECT
            a.title,
            au.name AS author_name
        FROM form_lab_simplearticle AS a
        INNER JOIN form_lab_author AS au
            ON a.author_id = au.id
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    result: List[ArticleAuthorRow] = []

    for row in rows:
        raw_data: ArticleAuthorRow = {
            "title": row[0],
            "author_name": row[1],
        }

        validated = ArticleAuthorSchema(**raw_data)

        result.append(
            {
                "title": validated.title,
                "author_name": validated.author_name,
            }
        )

    return result


def fetch_articles_with_authors_left() -> List[ArticleAuthorRow]:
    """
    Articleを基準にLEFT JOINして
    Authorがなくても記事を取得する
    """

    query: str = """
        SELECT
            a.title,
            au.name AS author_name
        FROM form_lab_simplearticle AS a
        LEFT JOIN form_lab_author AS au
            ON a.author_id = au.id
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    result: List[ArticleAuthorRow] = []

    for row in rows:
        raw_data: ArticleAuthorRow = {
            "title": row[0],
            "author_name": row[1],
        }

        validated = ArticleAuthorSchema(**raw_data)

        result.append(
            {
                "title": validated.title,
                "author_name": validated.author_name,
            }
        )

    return result
