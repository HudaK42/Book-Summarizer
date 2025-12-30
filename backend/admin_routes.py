from flask import Blueprint, jsonify, session
from utils.database import get_db_connection

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/admin")


def admin_required():
    return session.get("role") == "admin"


# ---------------- View All Summaries ----------------

@admin_bp.route("/summaries", methods=["GET"])
def view_all_summaries():
    if not admin_required():
        return jsonify({"error": "Unauthorized"}), 403

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            s.summary_id,
            u.name AS user_name,
            b.title AS book_title,
            LENGTH(s.summary_text) - LENGTH(REPLACE(s.summary_text, ' ', '')) + 1
                AS summary_word_count,
            s.model_used,
            s.processing_time,
            s.created_at
        FROM summaries s
        JOIN users u ON s.user_id = u.user_id
        JOIN books b ON s.book_id = b.book_id
        ORDER BY s.created_at DESC
    """)

    rows = cur.fetchall()
    conn.close()

    return jsonify({"summaries": [dict(row) for row in rows]}), 200


# ---------------- Delete Summary ----------------
@admin_bp.route("/delete-summary/<int:summary_id>", methods=["DELETE"])
def delete_summary(summary_id):
    if not admin_required():
        return jsonify({"error": "Unauthorized"}), 403

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM summaries WHERE summary_id=?", (summary_id,))
    conn.commit()
    conn.close()

    return jsonify({"status": "success"}), 200


# ---------------- Analytics ----------------
@admin_bp.route("/analytics", methods=["GET"])
def analytics():
    if not admin_required():
        return jsonify({"error": "Unauthorized"}), 403

    conn = get_db_connection()
    cur = conn.cursor()

    # Total summaries
    cur.execute("SELECT COUNT(*) FROM summaries")
    total_summaries = cur.fetchone()[0]

    # Average summary length (computed from text)
    cur.execute("""
        SELECT AVG(
            LENGTH(summary_text) - LENGTH(REPLACE(summary_text, ' ', '')) + 1
        )
        FROM summaries
    """)
    avg_length = round(cur.fetchone()[0] or 0, 2)

    # Most active users
    cur.execute("""
        SELECT u.name, COUNT(*) AS count
        FROM summaries s
        JOIN users u ON s.user_id = u.user_id
        GROUP BY s.user_id
        ORDER BY count DESC
        LIMIT 5
    """)
    most_active_users = [dict(row) for row in cur.fetchall()]

    # Most summarized books
    cur.execute("""
        SELECT b.title, COUNT(*) AS count
        FROM summaries s
        JOIN books b ON s.book_id = b.book_id
        GROUP BY s.book_id
        ORDER BY count DESC
        LIMIT 5
    """)
    most_summarized_books = [dict(row) for row in cur.fetchall()]

    conn.close()

    return jsonify({
        "total_summaries": total_summaries,
        "avg_summary_length": avg_length,
        "most_active_users": most_active_users,
        "most_summarized_books": most_summarized_books
    }), 200


@admin_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"status": "success"}), 200
