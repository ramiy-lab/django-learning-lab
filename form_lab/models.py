from __future__ import annotations

from django.db import models


class Author(models.Model):
    name: models.CharField[str, str] = models.CharField(
        max_length=100,
        unique=True,
    )

    def __str__(self) -> str:
        return str(self.name)


class SimpleArticle(models.Model):
    title: models.CharField[str, str] = models.CharField(
        max_length=200,
    )
    body: models.TextField[str, str] = models.TextField()
    author: models.ForeignKey[Author, Author] = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
    )
    body_length: models.IntegerField[int, int] = models.IntegerField(
        null=True,
        default=0,
    )

    def __str__(self) -> str:
        return str(self.title)
