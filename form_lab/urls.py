from django.urls import path
from . import views

app_name = "form_lab"

urlpatterns = [
    path(
        "articles/create/",
        views.article_create_view,
        name="article_create",
    ),
    path(
        "articles/",
        views.article_list_view,
        name="article_list",
    ),
    path(
        "articles/<int:article_id>/update/",
        views.article_update_view,
        name="article_update",
    ),
    path(
        "articles/<int:article_id>/delete/",
        views.article_delete_view,
        name="article_delete",
    ),
]
