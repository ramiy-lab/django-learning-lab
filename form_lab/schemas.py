from pydantic import BaseModel


class ArticleSchema(BaseModel):
    title: str
    body: str
    author_name: str


class ArticleAuthorSchema(BaseModel):
    title: str
    author_name: str | None
