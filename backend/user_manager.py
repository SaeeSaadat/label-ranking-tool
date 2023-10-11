from database_manager import get_db_cursor


def does_user_exist(username: str) -> bool:
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchone() is not None


def get_user_answer_count(username: str) -> int:
    with get_db_cursor() as cursor:
        cursor.execute("SELECT COUNT(DISTINCT row_num) FROM submissions WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result is None:
            return 0
        return result[0]


def get_user_group(username: str) -> int:
    with get_db_cursor() as cursor:
        cursor.execute("SELECT group_id FROM users where username = ?", (username, ))
        return cursor.fetchone()[0]


if __name__ == '__main__':
    print(get_user_group('user2'))
