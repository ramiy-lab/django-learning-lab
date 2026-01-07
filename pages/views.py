from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .services import build_page_context


def home(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello Django")


def page_detail(request: HttpRequest, id: int) -> HttpResponse:
    # 1. request は「入力」
    method = request.method  # GET / POST など

    # 2. Service層を呼ぶ（責務はここにない）
    context = build_page_context(page_id=id)

    # 3. responseを返す（出力）
    return render(request, "pages/detail.html", context)
