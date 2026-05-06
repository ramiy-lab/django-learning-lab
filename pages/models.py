from __future__ import annotations

from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.name)


class Article(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="タイトル",
    )

    body = models.TextField(
        blank=True,
        verbose_name="本文",
    )

    user: models.ForeignKey[User] = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="articles",
        null=True,
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="作成日時",
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return str(self.title)
