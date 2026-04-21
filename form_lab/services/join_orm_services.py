from __future__ import annotations

from typing import List

from ..models import SimpleArticle
from ..types import ArticleAuthorRow
from ..schemas import ArticleAuthorSchema


def fetch_article_with_authors() -> List[ArticleAuthorRow]:
    """
    ArticleとAuthorをselect_relatedで取得し
    titleとauthor_nameを返す
    """

    articles = SimpleArticle.objects.select_related("author").all()

    result: List[ArticleAuthorRow] = []

    for article in articles:
        raw_data: ArticleAuthorRow = {
            "title": article.title,
            "author_name": article.author.name,
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
    Articleを基準に取得し、
    Authorがなくても記事を取得する (LEFT JOIN的挙動)
    """

    articles = SimpleArticle.objects.select_related("author").all()

    result: List[ArticleAuthorRow] = []

    for article in articles:
        raw_data: ArticleAuthorRow = {
            "title": article.title,
            "author_name": article.author.name if article.author else None,
        }

        validated = ArticleAuthorSchema(**raw_data)

        result.append(
            {
                "title": validated.title,
                "author_name": validated.author_name,
            }
        )

    return result
