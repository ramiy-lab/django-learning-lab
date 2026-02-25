from django.urls import path
from . import views

app_name = "form_lab"

urlpatterns = [
    path(
        "simple/",
        views.article_create,
        name="article_create",
    ),
]
