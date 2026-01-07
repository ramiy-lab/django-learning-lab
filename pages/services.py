from typing import Any


def build_page_context(*, page_id: int, debug: bool) -> dict[str, Any]:
    """
    表示専用のcontextを組み立てるService
    """
    context: dict[str, Any] = {
        "page_id": page_id,
        "message": f"Page ID is {page_id}",
        "debug": debug,
    }

    if debug:
        context["debug_message"] = "Debug mode is ON"

    return context
