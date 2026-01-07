def build_page_context(page_id: int) -> dict[str, int]:
    """
    ページ表示に必要な際小コンテキストを作る
    """
    return {
        "page_id": page_id,
    }
