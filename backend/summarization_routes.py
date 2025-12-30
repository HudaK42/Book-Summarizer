# from flask import Blueprint, request, jsonify, session
# from utils.database import get_db_connection
# import time,json
# from models.summarization_model import summarize_text
# from backend.chunking import smart_chunk_text, merge_chunk_summaries

# summary_bp = Blueprint("summary_bp", __name__)

# @summary_bp.route("/summarize", methods=["POST"])
# def summarize_book():
#     user_id = session.get("user_id")
#     if not user_id:
#         return jsonify({"error": "Unauthorized"}), 401

#     data = request.json
#     if not data or "text" not in data:
#         return jsonify({"error": "Missing book text"}), 400

#     book_text = data["text"]
#     book_id = data.get("book_id")
#     summary_style = data.get("summary_style", "paragraphs")
#     summary_length = data.get("summary_length", "medium")

#     start_time = time.time()

#     try:
#         # 1️⃣ CHUNKING (Task 10)
#         chunk_data = smart_chunk_text(
#             book_text,
#             max_words=1000,
#             overlap=150
#         )

#         chunks = chunk_data["chunks"]
#         total_chunks = chunk_data["total_chunks"]

#         chunk_summaries = []

#         # 2️⃣ SUMMARIZE EACH CHUNK (Task 9)
#         for chunk in chunks:
#             summary, _ = summarize_text(chunk["text"])
#             if not summary:
#                 summary = "[Summary unavailable for this section]"
#             chunk_summaries.append({
#                 "chunk_id": chunk["chunk_id"],
#                 "summary": summary
#             })

#         # 3️⃣ MERGE SUMMARIES (ORDER + CONTEXT PRESERVED)
#         final_summary = merge_chunk_summaries(chunk_summaries)

#         # 4️⃣ SAVE TO DB
#         if book_id:
#             conn = get_db_connection()
#             cur = conn.cursor()
#             cur.execute(
#                 """
#                 INSERT INTO summaries
#                 (book_id, user_id, summary_text, summary_length, summary_style, chunk_summaries, processing_time)
#                 VALUES (?, ?, ?, ?, ?, ?, ?)
#                 """,
#                 (
#                     book_id,
#                     user_id,
#                     final_summary,
#                     summary_length,
#                     summary_style,
#                     json.dumps({
#                         "total_chunks": total_chunks,
#                         "chunks": chunk_summaries
#                     }),
#                     round(time.time() - start_time, 2)
#                 )
#             )
#             conn.commit()
#             conn.close()

#         return jsonify({
#             "status": "success",
#             "total_chunks": total_chunks,
#             "summary": final_summary,
#             "processing_time": round(time.time() - start_time, 2)
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# backend/summarization_routes.py

from flask import Blueprint, request, jsonify, session
from utils.database import get_db_connection
from models.summarization_model import summarize_text
from utils.summary_versioning import get_next_version
import time
import logging

# -----------------------------------------
# Blueprint
# -----------------------------------------
summary_bp = Blueprint("summary_bp", __name__)

# -----------------------------------------
# Logging
# -----------------------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# -----------------------------------------
# UI → Model Parameter Mapping
# -----------------------------------------
def get_summary_params(summary_length, detail_level):
    if summary_length == "short":
        max_output = 180
    elif summary_length == "long":
        max_output = 450
    else:
        max_output = 300  # medium

    if detail_level == "detailed":
        max_output += 120

    return max_output


def format_summary_style(summary_text, style):
    if style == "bullets":
        sentences = [s.strip() for s in summary_text.split(".") if s.strip()]
        return "\n".join(f"- {s}" for s in sentences)
    return summary_text


# -----------------------------------------
# Main Summarization API
# -----------------------------------------
@summary_bp.route("/summarize", methods=["POST"])
def summarize_book():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    logger.info(
        f"Summarize request | user_id={user_id} | payload_keys={list(data.keys())}"
    )

    # -----------------------------------------
    # Input Handling
    # -----------------------------------------
    book_id = data.get("book_id")
    book_text = data.get("text") if not book_id else None

    # -----------------------------------------
    # Fetch book text if uploaded book selected
    # -----------------------------------------
    if book_id and not book_text:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT original_text FROM books WHERE book_id=? AND user_id=?",
            (book_id, user_id)
        )
        row = cur.fetchone()
        conn.close()

        if not row:
            return jsonify({"error": "Book not found"}), 404

        book_text = row["original_text"]

        if not book_text.strip():
            return jsonify({"error": "Book text is empty"}), 400

    if not book_text:
        return jsonify({"error": "Missing text to summarize"}), 400

    # -----------------------------------------
    # UI Options
    # -----------------------------------------
    summary_length = data.get("summary_length", "medium")
    summary_style = data.get("summary_style", "paragraphs")
    detail_level = data.get("detail_level", "concise")

    max_output_length = get_summary_params(summary_length, detail_level)

    # -----------------------------------------
    # Summarization
    # -----------------------------------------
    try:
        start_time = time.time()

        final_summary, _, total_chunks = summarize_text(
            book_text,
            max_output_length=max_output_length
        )

        if not final_summary:
            return jsonify({"error": "Summarization failed"}), 500

        # Post-processing
        from backend.post_processing import refine_summary
        final_summary = refine_summary(final_summary, max_words=max_output_length)
        final_summary = format_summary_style(final_summary, summary_style)

        processing_time = round(time.time() - start_time, 2)

        summary_id = None

        # -----------------------------------------
        # Save summary ONLY for uploaded books
        # -----------------------------------------
        if book_id:
            version = get_next_version(book_id, user_id)

            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute(
                """
                INSERT INTO summaries
                (book_id, user_id, summary_text, summary_length,
                 summary_style, detail_level, model_used,
                 version, processing_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    book_id,
                    user_id,
                    final_summary,
                    summary_length,
                    summary_style,
                    detail_level,
                    "distilbart-cnn-12-6",
                    version,
                    processing_time
                )
            )

            summary_id = cur.lastrowid

            # ✅ IMPORTANT: update book status
            cur.execute(
                "UPDATE books SET status='completed' WHERE book_id=? AND user_id=?",
                (book_id, user_id)
            )

            conn.commit()
            conn.close()

        # -----------------------------------------
        # Response
        # -----------------------------------------
        return jsonify({
            "status": "success",
            "summary": final_summary,
            "summary_id": summary_id,
            "total_chunks": total_chunks,
            "processing_time": processing_time
        })

    except Exception as e:
        logger.exception("🔥 Backend summarization error")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
