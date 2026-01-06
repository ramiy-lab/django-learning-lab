from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello Django")


def page_detail(request: HttpRequest, id: int) -> HttpResponse:
    context = {
        "page_id": id,
    }
    return render(request, "pages/detail.html", context)
