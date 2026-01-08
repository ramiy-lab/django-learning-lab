from django.db import models


class Page(models.Model):  # type: ignore[misc]
    title = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self) -> str:
        return str(self.title)
