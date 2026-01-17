from email.policy import default
from django.db import models


class Article(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="タイトル",
    )

    subtitle = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="サブタイトル",
    )

    body = models.TextField(
        verbose_name="本文",
    )

    view_count = models.IntegerField(
        default=0,
        verbose_name="閲覧数",
    )

    def __str__(self):
        return self.title
