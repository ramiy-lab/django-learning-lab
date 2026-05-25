from typing import Any

import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from pages.models import Article


@pytest.mark.django_db
def test_article_list_view_get(
    client: Client,
    article: Article,
) -> None:
    """
    ArticleListView が正常表示されることを確認する
    """

    url = reverse("pages:article_list")

    response = client.get(url)

    assert response.status_code == 200

    assertTemplateUsed(
        response,
        "pages/article_list.html",
    )

    assert response.context["page_title"] == "Public Article List"

    assert response.context["article_count"] == 1

    article_list: Any = response.context["articles"]

    assert len(article_list) == 1

    assert article_list[0] == article
