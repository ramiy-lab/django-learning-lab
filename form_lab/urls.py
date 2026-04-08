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
        views.article_list_plain_view,
        name="article_list_plain",
    ),
    path(
        "articles/with-author/",
        views.article_list_with_author_view,
        name="article_list_with_author",
    ),
    path(
        "articles/with-author-left/",
        views.article_list_with_author_left_view,
        name="article_list_with_author_left",
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
