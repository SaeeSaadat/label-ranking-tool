from database_manager import get_db_cursor


def does_user_exist(username: str) -> bool:
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchone() is not None
