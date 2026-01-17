from django.db import models


class Article(models.Model):  # type: ignore[misc]
    title = models.CharField(max_length=100)
    body = models.TextField()
    views = models.IntegerField()

    def __str__(self):
        return self.title
