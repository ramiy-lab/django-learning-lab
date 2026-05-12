from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)

from pages.models import Article
from pages.forms import (
    ArticleCreateForm,
    ContactForm,
)
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

    can_add_article: bool = request.user.has_perm("pages.add_article")

    can_change_article: bool = request.user.has_perm("pages.change_article")

    can_delete_article: bool = request.user.has_perm("pages.delete_article")

    context = {
        "can_add_article": can_add_article,
        "can_change_article": can_change_article,
        "can_delete_article": can_delete_article,
    }

    return render(
        request,
        "pages/dashboard.html",
        context,
    )


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


@login_required
def admin_only_view(request: HttpRequest) -> HttpResponse:
    """
    管理者専用ページ
    """
    if not request.user.has_perm("pages.delete_article"):
        raise PermissionDenied

    return render(
        request,
        "pages/admin_only.html",
    )


class HelloView(View):
    """
    最小CBVサンプル
    """

    def get(
        self,
        request: HttpRequest,
    ) -> HttpResponse:
        return render(
            request,
            "pages/cbv_hello.html",
        )


class AboutPageView(TemplateView):
    """
    テンプレート表示専用CBV
    """

    template_name = "pages/about.html"


class ArticleListView(ListView):
    """
    Article一覧表示CBV
    """

    model = Article

    template_name = "pages/article_list.html"

    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.filter(
            user=self.request.user,
        )


class ArticleCreateView(CreateView):
    """
    Article作成CBV
    """

    form_class = ArticleCreateForm

    template_name = "pages/article_create.html"

    success_url = reverse_lazy("pages:article_list")

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    """
    Article更新CBV
    """

    model = Article

    form_class = ArticleCreateForm

    template_name = "pages/article_update.html"

    success_url = reverse_lazy("pages:article_list")

    context_object_name = "article"

    def get_queryset(self):
        return Article.objects.filter(
            user=self.request.user,
        )

    def form_valid(self, form):
        return super().form_valid(form)


class ArticleDeleteView(DeleteView):
    """
    Article削除CBV
    """

    model = Article

    template_name = (
        "pages/article_confirm_delete.html"
    )

    success_url = reverse_lazy(
        "pages:article_list"
    )

    context_object_name = "article"

    def get_queryset(self):
        return Article.objects.filter(
            user=self.request.user,
        )


class ContactFormView(FormView):
    """
    Contact FormView
    """

    form_class = ContactForm

    template_name = "pages/contact.html"

    success_url = reverse_lazy(
        "pages:article_list"
    )

    def form_valid(self, form):
        print("=== CONTACT FORM ===")

        print(
            form.cleaned_data["name"]
        )

        print(
            form.cleaned_data["email"]
        )

        print(
            form.cleaned_data["message"]
        )

        return super().form_valid(form)
