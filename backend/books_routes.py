import os
from flask import Blueprint, request, jsonify, session
from utils.database import get_db_connection

books_bp = Blueprint("books_bp", __name__)



@books_bp.route("/books", methods=["GET"])
def get_books():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # -------- Query params --------
    q = request.args.get("q", "").strip()
    sort = request.args.get("sort", "newest")
    status = request.args.get("status")  # summarized / not_summarized
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))
    offset = (page - 1) * limit

    # -------- Base query --------
    query = """
        SELECT
            book_id,
            title,
            author,
            upload_date,
            status
        FROM books
        WHERE user_id = ?
    """

    params = [user_id]

    # -------- Search --------
    if q:
        query += " AND (title LIKE ? OR author LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%"])

    # -------- Filter --------
    if status == "summarized":
        query += " AND status = 'completed'"
    elif status == "not_summarized":
        query += " AND status != 'completed'"

    # -------- Sort --------
    if sort == "oldest":
        query += " ORDER BY upload_date ASC"
    elif sort == "az":
        query += " ORDER BY title ASC"
    else:
        query += " ORDER BY upload_date DESC"  # newest default

    # -------- Pagination --------
    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()

    # -------- Total count --------
    cur.execute(
        "SELECT COUNT(*) FROM books WHERE user_id = ?",
        (user_id,)
    )
    total = cur.fetchone()[0]

    conn.close()

    return jsonify({
        "books": [dict(row) for row in rows],
        "page": page,
        "limit": limit,
        "total": total
    })


@books_bp.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM books WHERE book_id=? AND user_id=?",
        (book_id, user_id)
    )
    book = cur.fetchone()
    conn.close()

    if not book:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(dict(book))


@books_bp.route("/books/<int:book_id>/summarize", methods=["POST"])
def summarize_book(book_id):
    user_id = session.get("user_id")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE books SET status='processing' WHERE book_id=? AND user_id=?",
        (book_id, user_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Summarization started"})


@books_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    user_id = session.get("user_id")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT file_path FROM books WHERE book_id=? AND user_id=?",
        (book_id, user_id)
    )
    book = cur.fetchone()

    if not book:
        return jsonify({"error": "Not found"}), 404

    if book["file_path"] and os.path.exists(book["file_path"]):
        os.remove(book["file_path"])

    cur.execute(
        "DELETE FROM books WHERE book_id=? AND user_id=?",
        (book_id, user_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Book deleted"})
