from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Page
from .services import process_comment


def page_detail(request, id: int):
    page = get_object_or_404(Page, id=id)

    message = ""

    if request.method == "POST":
        comment = request.POST.get("comment", "")
        message = process_comment(comment)

    context = {
        "page": page,
        "message": message,
    }
    return render(request, "pages/detail.html", context)
