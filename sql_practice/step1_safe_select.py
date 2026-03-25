from typing import Any, Sequence

from django.db import connection


def fetch_users_by_id(*, user_id: int) -> list[tuple[Any, ...]]:
    """
    指定したユーザーIDのレコードを取得する

    安全なSQL実行の基本形：
    ・%s プレースホルダ使用
    ・paramsで値を渡す
    """

    query: str = "SELECT id, username FORM auth_user WHERE id = %s"
    params: Sequence[Any] = [user_id]

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        rows: list[tuple[Any, ...]] = cursor.fetchall()

    return rows


def main() -> None:
    """
    動作確認用エントリポイント
    """

    user_id: int = 1
    results: list[tuple[Any, ...]] = fetch_users_by_id(user_id=user_id)

    for row in results:
        print(row)


if __name__ == "__main__":
    main()
