from typing import TypedDict


class ArticleInput(TypedDict):
    title: str
    body: str
    author_name: str


class ArticleAuthorRow(TypedDict):
    title: str
    author_name: str | None
