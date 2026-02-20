from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import SimpleArticleForm


def simple_article_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SimpleArticleForm(request.POST)

        if form.is_valid():
            article = form.save()
            print("保存されたID", article.id)

    else:
        form = SimpleArticleForm()

    return render(request, "form_lab/simple_article_form.html", {"form": form})
