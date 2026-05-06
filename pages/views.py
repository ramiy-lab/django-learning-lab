from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from pages.models import Article
from pages.services import (
    process_comment,
    create_article,
    list_articles_by_user,
    get_article_by_user,
)
from pages.types import ArticleInput


def page_detail(request: HttpRequest, id: int) -> HttpResponse:
    page = get_object_or_404(Article, id=id)

    message: str = ""

    if request.method == "POST":
        comment: str = request.POST.get("comment", "")
        message = process_comment(comment)

        request.session["message"] = message
        return redirect("pages:detail", id=page.id)

    message = request.session.pop("message", "")

    context = {
        "page": page,
        "message": message,
    }
    return render(request, "pages/detail.html", context)


def dashboard_view(request: HttpRequest) -> HttpResponse:
    """
    ダッシュボード (ログイン後の起点ページ)
    """
    print("=== request.user debug ===")
    print("user:", request.user)
    print("type:", type(request.user))
    print("is_authenticated:", request.user.is_authenticated)
    print("==========================")

    return render(request, "pages/dashboard.html")


@login_required
def home_view(request: HttpRequest) -> HttpResponse:
    """
    ホーム画面 (サブページ)
    """
    return render(request, "pages/home.html")


@login_required
def mypage_view(request: HttpRequest) -> HttpResponse:
    """
    自分の記事一覧
    """
    assert isinstance(request.user, User)

    articles = list_articles_by_user(user=request.user)
    return render(
        request,
        "pages/mypage.html",
        {"articles": articles},
    )


@login_required
def create_article_view(request: HttpRequest) -> HttpResponse:
    """
    記事作成 (超シンプル版)
    """

    assert isinstance(request.user, User)

    if request.method == "POST":
        title: str = request.POST.get("title", "")
        body: str = request.POST.get("body", "")

        data: ArticleInput = {
            "title": title,
            "body": body,
        }

        create_article(user=request.user, data=data)
        return redirect("pages:mypage")

    return render(request, "pages/create_article.html")


@login_required
def article_detail_view(request: HttpRequest, article_id: int) -> HttpResponse:
    """
    記事詳細 (自分のものだけ)
    """
    assert isinstance(request.user, User)

    article = get_article_by_user(
        user=request.user,
        article_id=article_id,
    )

    return render(
        request,
        "pages/article_detail.html",
        {"article": article},
    )
