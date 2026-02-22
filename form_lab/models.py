from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.name)


class SimpleArticle(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return str(self.title)
