from pydantic import BaseModel


class ArticleSchema(BaseModel):
    title: str

    body: str
