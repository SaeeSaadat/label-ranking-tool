import logging
import sqlite3

LIMIT = 150


def main():
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()
    query = "select row_num, username, answers from submissions;"
    cursor.execute(query)
    result = cursor.fetchall()
    counter = 0
    for row_num, username, answers in result:
        answers = answers.split(',')
        if answers[1] == '7' or answers[2] == '7':
            print(f"Row {row_num} by {username} is being pruned. prv answers: {answers}")
            cursor.execute("delete from submissions where row_num = ? and username = ?", (row_num, username))
            counter += 1
        if counter >= LIMIT:
            break
    print(f"Pruned {counter} rows from submissions table!")

    connection.commit()
    connection.close()

if __name__ == '__main__':
    main()