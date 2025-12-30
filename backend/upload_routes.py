from flask import Blueprint, request, jsonify, session
import os
from werkzeug.utils import secure_filename
from utils.database import get_db_connection
from backend.text_extractor import extract_text
from backend.text_preprocessor import process_text_pipeline



# -------------------------------------------------
# CREATE BLUEPRINT
# -------------------------------------------------
upload_bp = Blueprint("upload_bp", __name__)

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
UPLOAD_FOLDER = "data/uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# -------------------------------------------------
# UPLOAD FILE
# -------------------------------------------------
@upload_bp.route("/upload_file", methods=["POST"])
def upload_file():
    user_id = session.get("user_id") or 1
    file = request.files.get("file")

    if not user_id:
        return jsonify({"status": "error", "message": "User ID missing"}), 400

    if not file or not allowed_file(file.filename):
        return jsonify({"status": "error", "message": "Invalid file"}), 400

    # File size check
    file.seek(0, os.SEEK_END)
    if file.tell() > MAX_FILE_SIZE:
        return jsonify({"status": "error", "message": "Max file size is 10MB"}), 400
    file.seek(0)

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    # -------- TEXT EXTRACTION --------
    extracted = extract_text(path)
    raw_text = extracted.get("text", "").strip()

    if not raw_text:
        return jsonify({"status": "error", "message": "No text extracted"}), 400

    # -------- TASK-6 PIPELINE --------
    processed = process_text_pipeline(raw_text)
    
    cleaned_text = processed["cleaned_text"]  # ✅ add this

    title = request.form.get("title", "").strip() or os.path.splitext(filename)[0]
    author = request.form.get("author", "").strip()
    # chapter = request.form.get("chapter", "").strip()

    conn = get_db_connection()
    cur = conn.cursor()

    
    file_ext = os.path.splitext(filename)[1].lower().replace(".", "")

    cur.execute(
    """
    INSERT INTO books (
        user_id,
        author,
        title,
        original_text,
        file_type,status
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        user_id,
        author,
        title,
        cleaned_text,
        file_ext,
        "uploaded"
    ),
)

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "File uploaded successfully",
        "language": processed["language"],
        "total_chunks": processed["total_chunks"]
    })


@upload_bp.route("/books/paginated", methods=["GET"])
def paginated_books():
    user_id = session.get("user_id")  or 1
    page_no = int(request.args.get("page_no", 1))
    limit = int(request.args.get("limit", 5))
    offset = (page_no - 1) * limit

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM books WHERE user_id = ? LIMIT ? OFFSET ?",
        (user_id, limit, offset)
    )
    rows = cur.fetchall()
    conn.close()

    return jsonify([dict(r) for r in rows])

@upload_bp.route("/submit_text", methods=["POST"])
def submit_text():
    user_id = session.get("user_id") or 1
    data = request.get_json()

    if not data or not data.get("text"):
        return jsonify({"status": "error", "message": "Text missing"}), 400

    raw_text = data["text"].strip()

    processed = process_text_pipeline(raw_text)
    cleaned_text = processed["cleaned_text"]

    title = data.get("title", "Untitled")
    author = data.get("author", "")

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO books (user_id, author, title, original_text, file_type, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            author,
            title,
            cleaned_text,
            "text",
            "uploaded"
        ),
    )

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Text submitted successfully",
        "language": processed["language"],
        "total_chunks": processed["total_chunks"]
    })
