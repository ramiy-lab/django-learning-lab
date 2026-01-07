from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .services import build_page_context


def page_detail(request: HttpRequest, id: int) -> HttpResponse:
    # GETパラメータは文字列として入る
    debug_param: str | None = request.GET.get("debug")

    debug: bool = debug_param == "true"

    context = build_page_context(
        page_id=id,
        debug=debug,
    )

    return render(request, "pages/detail.html", context)
