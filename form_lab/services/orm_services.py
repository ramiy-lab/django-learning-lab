from typing import List, Tuple

from django.db import transaction
from django.db.models import Count, Sum, Avg

from ..models import Author, SimpleArticle
from ..types import ArticleInput
from ..schema import ArticleSchema


def create_article(*, data: ArticleInput) -> SimpleArticle:
    """
    ORMで記事を作成するService関数
    """
    validated = ArticleSchema(**data)

    body_length: int = len(validated.body)

    with transaction.atomic():
        author, _created = Author.objects.get_or_create(name=validated.author_name)

        article: SimpleArticle = SimpleArticle.objects.create(
            title=validated.title,
            body=validated.body,
            author=author,
            body_length=body_length,
        )

    return article


def list_articles() -> List[Tuple[int, str, str]]:
    """
    記事一覧を取得する (ORM SELECT)
    """

    articles = SimpleArticle.objects.all().order_by("-id")

    rows: List[Tuple[int, str, str]] = [
        (article.id, article.title, article.body) for article in articles
    ]

    return rows


def update_article(*, article_id: int, data: ArticleInput) -> SimpleArticle:
    """
    記事を更新する (ORM UPDATE)
    """

    validated = ArticleSchema(**data)

    body_length: int = len(validated.body)

    with transaction.atomic():
        author, _created = Author.objects.get_or_create(name=validated.author_name)

        article: SimpleArticle = SimpleArticle.objects.get(id=article_id)

        article.title = validated.title
        article.body = validated.body
        article.author = author
        article.body_length = body_length

        article.save()

    return article


def delete_article(*, article_id: int) -> None:
    """
    記事を削除する (ORM DELETE)
    """

    with transaction.atomic():
        article: SimpleArticle = SimpleArticle.objects.get(id=article_id)
        article.delete()


def get_article_stats() -> Tuple[int, int, float]:
    """
    ORMで集計を取得する
    """

    result = SimpleArticle.objects.aggregate(
        article_count=Count("id"),
        total_length=Sum("body_length"),
        avg_length=Avg("body_length"),
    )

    article_count: int = int(result["article_count"] or 0)
    total_length: int = int(result["total_length"] or 0)
    avg_length: float = float(result["avg_length"] or 0.0)

    return (article_count, total_length, avg_length)


def get_article_stats_by_author() -> List[Tuple[str, int, float]]:
    """
    ORMで著者ごとの集計を取得する
    """

    results = (
        SimpleArticle.objects.values("author__name")
        .annotate(
            article_count=Count("id"),
            avg_length=Avg("body_length"),
        )
        .order_by("-article_count")
    )

    return [
        (
            row["author__name"],
            row["article_count"],
            row["avg_length"],
        )
        for row in results
    ]


def get_popular_authors(*, min_articles: int) -> List[Tuple[str, int]]:
    """
    記事数が min_articles 件以上の著者を取得する (ORM)
    """

    results = (
        SimpleArticle.objects
        .values("author__name")
        .annotate(article_count=Count("id"))
        .filter(article_count__gte=min_articles)
        .order_by("-article_count")
    )

    return [(row["author__name"], int(row["article_count"])) for row in results]
