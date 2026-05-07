from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    page_detail,
    dashboard_view,
    home_view,
    mypage_view,
    create_article_view,
    article_detail_view,
    admin_only_view,
)

app_name = "pages"

urlpatterns = [
    path("pages/<int:id>/", page_detail, name="detail"),
    path(
        "login/",
        LoginView.as_view(template_name="pages/login.html"),
        name="login",
    ),
    path(
        "dashboard/",
        dashboard_view,
        name="dashboard",
    ),
    path(
        "home/",
        home_view,
        name="home",
    ),
    path(
        "mypage/",
        mypage_view,
        name="mypage",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        "articles/create/",
        create_article_view,
        name="article_create",
    ),
    path(
        "articles/<int:article_id>/",
        article_detail_view,
        name="article_detail",
    ),
    path(
        "admin-only/",
        admin_only_view,
        name="admin_only",
    ),
]
