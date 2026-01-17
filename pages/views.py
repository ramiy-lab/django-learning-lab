from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Article
from .services import process_comment


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
