from email.policy import default
from django.db import models


class Author(models.Model):  # type: ignore[misc]
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.name)


class Article(models.Model):  # type: ignore[misc]
    title = models.CharField(
        max_length=100,
        verbose_name="タイトル",
    )

    body = models.TextField(
        verbose_name="本文",
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="articles",
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return str(self.title)
