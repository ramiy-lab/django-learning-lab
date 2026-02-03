import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db.sqlite3"


def main() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                id,
                title,
                body,
                author_id,
                created_at
            FROM pages_articles
            ORDER BY id DESC
            LIMIT 5;
            """
        )
        rows = cursor.fetchall()

        for row in rows:
            print(row)


if __name__ == "__main__":
    main()
