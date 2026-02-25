from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import SimpleArticleForm


def article_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form: SimpleArticleForm = SimpleArticleForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect("form_lab:article_create")
    else:
        form = SimpleArticleForm()

    return render(
        request,
        "form_lab/simple_article_form.html",
        {"form": form},
    )
