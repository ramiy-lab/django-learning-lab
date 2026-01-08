from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Page
from .services import process_comment


def page_detail(request: HttpRequest, id: int) -> HttpResponse:
    page = get_object_or_404(Page, id=id)

    message = ""
    debug = False

    if request.method == "POST":
        comment = request.POST.get("comment", "")
        message = process_comment(comment)

    if request.GET.get("debug") == "true":
        debug = True

    context = {
        "page": page,
        "message": message,
        "debug": debug,
    }
    return render(request, "pages/detail.html", context)
