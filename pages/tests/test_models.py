from typing import Final

import pytest
from django.contrib.auth import get_user_model

from pages.models import Article

UserModel = get_user_model()

TEST_USERNAME: Final[str] = "test_user"
TEST_PASSWORD: Final[str] = "test_password"
TEST_TITLE: Final[str] = "pytest article"
TEST_BODY: Final[str] = "pytest body"


@pytest.mark.django_db
def test_article_create() -> None:
    """
    Article が正常作成されることを確認する
    """

    user = UserModel.objects.create_user(
        username=TEST_USERNAME,
        password=TEST_PASSWORD,
    )

    article = Article.objects.create(
        title=TEST_TITLE,
        body=TEST_BODY,
        user=user,
    )

    assert article.title == TEST_TITLE
    assert article.body == TEST_BODY


@pytest.mark.django_db
def test_article_str() -> None:
    """
    Article の __str__ が title を返すことを確認する
    """

    user = UserModel.objects.create_user(
        username=TEST_USERNAME,
        password=TEST_PASSWORD,
    )

    article = Article.objects.create(
        title=TEST_TITLE,
        body=TEST_BODY,
        user=user,
    )

    assert str(article) == TEST_TITLE


@pytest.mark.django_db
def test_article_user_fk() -> None:
    """
    Article が正しい user を保存することを確認する
    """

    user = UserModel.objects.create_user(
        username=TEST_USERNAME,
        password=TEST_PASSWORD,
    )

    article = Article.objects.create(
        title=TEST_TITLE,
        body=TEST_BODY,
        user=user,
    )

    assert article.user == user


@pytest.mark.django_db
def test_article_saved_to_db() -> None:
    """
    ArticleがDBへ保存されることを確認する
    """

    user = UserModel.objects.create_user(
        username=TEST_USERNAME,
        password=TEST_PASSWORD,
    )

    Article.objects.create(
        title=TEST_TITLE,
        body=TEST_BODY,
        user=user,
    )

    assert Article.objects.count() == 1
