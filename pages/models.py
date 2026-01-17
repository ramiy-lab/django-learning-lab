from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()

    subtitle = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    view_count = models.IntegerField()

    def __str__(self):
        return self.title
