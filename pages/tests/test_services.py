from typing import Final

import pytest
from django.contrib.auth import get_user_model

from pages.models import Article
from pages.services import (
    create_article,
    delete_article,
    update_article,
)
from pages.types import ArticleInput


UserModel = get_user_model()

TEST_USERNAME: Final[str] = "service_user"
TEST_PASSWORD: Final[str] = "service_password"

CREATE_TITLE: Final[str] = "created title"
CREATE_BODY: Final[str] = "created body"

UPDATED_TITLE: Final[str] = "updated title"
UPDATED_BODY: Final[str] = "updated body"


@pytest.mark.django_db
def test_create_article() -> None:
    """
    create_article が正常に Article を作成することを確認する
    """

    user = UserModel.objects.create_user(
        username=TEST_USERNAME,
        password=TEST_PASSWORD,
    )

    article_input: ArticleInput = {
        "title": CREATE_TITLE,
        "body": CREATE_BODY,
    }

    article = create_article(
        user=user,
        data=article_input,
    )

    assert Article.objects.count() == 1

    assert article.title == CREATE_TITLE
    assert article.body == CREATE_BODY
    assert article.user == user


@pytest.mark.django_db
def test_update_article() -> None:
    """
    update_article が Article を正常更新することを確認する。
    """

    user = UserModel.objects.create_user(
        username=TEST_USERNAME,
        password=TEST_PASSWORD,
    )

    article = Article.objects.create(
        title=CREATE_TITLE,
        body=CREATE_BODY,
        user=user,
    )

    update_input: ArticleInput = {
        "title": UPDATED_TITLE,
        "body": UPDATED_BODY,
    }

    updated_article = update_article(
        article=article,
        data=update_input
    )

    article.refresh_from_db()

    assert updated_article.title == UPDATED_TITLE
    assert updated_article.body == UPDATED_BODY

    assert article.title == UPDATED_TITLE
    assert article.body == UPDATED_BODY


@pytest.mark.django_db
def test_delete_article() -> None:
    """
    delete_article が Article を正常削除することを確認する。
    """

    user = UserModel.objects.create_user(
        username=TEST_USERNAME,
        password=TEST_PASSWORD,
    )

    article = Article.objects.create(
        title=CREATE_TITLE,
        body=CREATE_BODY,
        user=user,
    )

    assert Article.objects.count() == 1

    delete_article(article=article)

    assert Article.objects.count() == 0
