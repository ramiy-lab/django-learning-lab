from __future__ import annotations

from typing import TypedDict


class ArticleInput(TypedDict):
    title: str
    body: str
    author_name: str


def handle_article_input(*, data: ArticleInput) -> None:
    """
    Formから渡された入力を受け取るService関数

    この段階ではDB操作は行わない
    """
    title: str = data["title"]
    body: str = data["body"]
    author_name: str = data["author_name"]

    # 確認用（今は処理しない）
    print(f"title={title}, body={body}, author={author_name}")
