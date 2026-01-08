from .models import Page


def build_page_context(page: Page, message: str = "") -> dict:
    return {
        "page": page,
        "message": message,
    }


def process_comment(comment: str) -> str:
    if not comment:
        return "コメントが入力されていません"

    if len(comment) > 100:
        return "コメントは100文字以内で入力してください"

    return "コメントを受け付けました"
