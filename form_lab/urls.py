from django.urls import path
from . import views

app_name = "form_lab"

urlpatterns = [
    path(
        "simple/",
        views.article_create_view,
        name="article_create",
    ),
]
