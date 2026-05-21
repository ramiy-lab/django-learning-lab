from __future__ import annotations

from typing import cast, Any

from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBase,
    HttpResponseRedirect,
)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.forms import Form
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
    DetailView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
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
    update_article,
    delete_article,
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


class ArticleListView(ListView[Article]):
    """
    Article一覧表示CBV
    """

    model = Article

    template_name = "pages/article_list.html"

    context_object_name = "articles"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        article_queryset: QuerySet[Article] = Article.objects.all()

        context["page_title"] = "Public Article List"
        context["article_count"] = article_queryset.count()

        return context


class ArticleCreateView(
    LoginRequiredMixin,
    CreateView[Article, ArticleCreateForm],
):
    """
    Article作成CBV
    """

    form_class = ArticleCreateForm

    template_name = "pages/article_create.html"

    success_url = reverse_lazy("pages:article_list")

    def form_valid(
        self,
        form: ArticleCreateForm
    ) -> HttpResponse:
        article_input: ArticleInput = {
            "title": form.cleaned_data["title"],
            "body": form.cleaned_data["body"],
        }

        user = cast(User, self.request.user)

        self.object = create_article(
            user=user,
            data=article_input,
        )

        return HttpResponseRedirect(self.get_success_url())


class ArticleUpdateView(
    LoginRequiredMixin,
    UpdateView[Article, ArticleCreateForm],
):
    """
    Article更新CBV
    """

    model = Article

    form_class = ArticleCreateForm

    template_name = "pages/article_update.html"

    context_object_name = "article"

    def get_queryset(self) -> QuerySet[Article]:
        return Article.objects.all()

    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        **kwargs: object
    ) -> HttpResponseBase:
        article = self.get_object()

        if (
            article.user != request.user
            and not request.user.is_superuser
        ):
            raise PermissionDenied

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )

    def form_valid(
        self,
        form: ArticleCreateForm
    ) -> HttpResponse:
        article_input: ArticleInput = {
            "title": form.cleaned_data["title"],
            "body": form.cleaned_data["body"],
        }

        self.object = update_article(
            article=self.get_object(),
            data=article_input,
        )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return str(reverse_lazy(
            "pages:article_detail",
            kwargs={"pk": self.object.pk},
        ))


class ArticleDeleteView(
    LoginRequiredMixin,
    DeleteView[Article, Any],
):
    """
    Article削除CBV
    """

    model = Article

    template_name = "pages/article_confirm_delete.html"

    success_url = str(reverse_lazy("pages:article_list"))

    context_object_name = "article"

    def get_queryset(self) -> QuerySet[Article]:
        if self.request.user.is_superuser:
            return Article.objects.all()

        return Article.objects.filter(
            user=self.request.user,
        )

    def delete(
            self,
            request: HttpRequest,
            *args: object,
            **kwargs: Any,
    ) -> HttpResponse:
        delete_article(
            article=self.get_object(),
        )

        return HttpResponseRedirect(self.get_success_url())


class ContactFormView(FormView[ContactForm]):
    """
    Contact FormView
    """

    form_class = ContactForm

    template_name = "pages/contact.html"

    success_url = str(reverse_lazy("pages:article_list"))

    def form_valid(
        self,
        form: ContactForm
    ) -> HttpResponse:
        print("=== CONTACT FORM ===")

        print(form.cleaned_data["name"])

        print(form.cleaned_data["email"])

        print(form.cleaned_data["message"])

        return super().form_valid(form)


class ArticleDetailView(
    LoginRequiredMixin,
    DetailView[Article],
):
    """
    Article詳細CBV
    """

    model = Article

    template_name = "pages/article_detail.html"

    context_object_name = "article"


class DashboardView(TemplateView):
    """
    ダッシュボード画面
    """

    template_name = "pages/dashboard.html"
