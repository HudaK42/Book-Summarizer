from utils.database import get_db_connection

def get_next_version(book_id, user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT MAX(version) FROM summaries
        WHERE book_id = ? AND user_id = ?
        """,
        (book_id, user_id)
    )

    row = cur.fetchone()
    conn.close()

    if row[0] is None:
        return 1
    return row[0] + 1
