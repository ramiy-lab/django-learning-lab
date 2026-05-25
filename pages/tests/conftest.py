from typing import Final

import pytest
from django.contrib.auth import get_user_model

from pages.models import Article


UserModel = get_user_model()

TEST_USERNAME: Final[str] = "fixture_user"
TEST_PASSWORD: Final[str] = "fixture_password"

TEST_TITLE: Final[str] = "fixture title"
TEST_BODY: Final[str] = "fixture body"


@pytest.fixture
def user():
    """
    テスト用 User を生成する fixture。
    """

    return UserModel.objects.create_user(
        username=TEST_USERNAME,
        password=TEST_PASSWORD,
    )


@pytest.fixture
def article(user):
    """
    テスト用 Article を生成する fixture
    """

    return Article.objects.create(
        title=TEST_TITLE,
        body=TEST_BODY,
        user=user,
    )
