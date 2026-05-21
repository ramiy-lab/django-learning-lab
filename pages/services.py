from __future__ import annotations

from typing import List

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from pages.models import Article
from pages.types import ArticleInput
from pages.schemas import ArticleSchema


def build_page_context(page: Article, message: str = "") -> dict[str, object]:
    return {
        "page": page,
        "message": message,
    }


def process_comment(comment: str) -> str:
    if not comment:
        return "コメントが入力されていません"

    if len(comment) > 100:
        return "コメントは100文字以内で入力してください"

    return f"コメントを受け付けました: {comment}"


# def create_article(*, user: User, data: ArticleInput) -> Article:
#     """
#     記事作成 (必ずuserを受け取る)
#     """
#     article: Article = Article.objects.create(
#         title=data["title"],
#         body=data["body"],
#         user=user,
#     )
#     return article


def list_articles_by_user(*, user: User) -> List[Article]:
    """
    自分のデータだけ取得
    """
    return list(Article.objects.filter(user=user).order_by("-created_at"))


def get_article_by_user(*, user: User, article_id: int) -> Article:
    """
    自分のデータだけを取得 (存在しなければ404)
    """
    article: Article = get_object_or_404(
        Article,
        id=article_id,
        user=user,
    )
    return article


def create_article(
    *,
    user: User,
    data: ArticleInput,
) -> Article:
    validated_data = ArticleSchema.model_validate(data)
    article = Article.objects.create(
        title=validated_data.title,
        body=validated_data.body,
        user=user,
    )

    return article


def update_article(
    *,
    article: Article,
    data: ArticleInput,
) -> Article:
    validated_date = ArticleSchema.model_validate(data)

    article.title = validated_date.title

    article.body = validated_date.body

    article.save()

    return article


def delete_article(
    *,
    article: Article,
) -> None:
    article.delete()
