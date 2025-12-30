from flask import Blueprint, jsonify, request, session
from utils.database import get_db_connection

summary_mgmt_bp = Blueprint(
    "summary_mgmt_bp",
    __name__,
    url_prefix="/summaries"
)

# ----------------------------------
# GET all summaries of a book
# ----------------------------------
@summary_mgmt_bp.route("/book/<int:book_id>", methods=["GET"])
def get_summaries(book_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            summary_id,
            summary_text,
            summary_length,
            summary_style,
            detail_level,
            model_used,
            version,
            processing_time,
            created_at
        FROM summaries
        WHERE book_id = ?
          AND user_id = ?
          AND is_deleted = 0
        ORDER BY version DESC
    """, (book_id, user_id))

    rows = cur.fetchall()
    conn.close()

    # Convert rows to list of dicts
    summaries_list = [dict(row) for row in rows] if rows else []

    return jsonify({"summaries": summaries_list}), 200


# ----------------------------------
# UPDATE summary
# ----------------------------------
@summary_mgmt_bp.route("/<int:summary_id>", methods=["PUT"])
def update_summary(summary_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    new_text = data.get("summary_text")
    if not new_text:
        return jsonify({"error": "Summary text required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE summaries
        SET summary_text = ?
        WHERE summary_id = ? AND user_id = ? AND is_deleted = 0
    """, (new_text, summary_id, user_id))

    conn.commit()
    conn.close()
    return jsonify({"status": "updated"}), 200


# ----------------------------------
# DELETE summary (Soft delete)
# ----------------------------------
@summary_mgmt_bp.route("/<int:summary_id>", methods=["DELETE"])
def delete_summary(summary_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE summaries
        SET is_deleted = 1
        WHERE summary_id = ? AND user_id = ?
    """, (summary_id, user_id))

    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"}), 200
