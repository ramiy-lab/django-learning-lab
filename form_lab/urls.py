from django.urls import path
from . import views

app_name = "form_lab"

urlpatterns = [
    path(
        "simple/",
        views.simple_article_create,
        name="simple_article_create",
    ),
]
