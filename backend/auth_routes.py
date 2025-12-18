# from flask import Blueprint, request, jsonify, session
# import bcrypt, time
# from utils.database import get_db_connection  # absolute import from project root

# auth_bp = Blueprint("auth_bp", __name__)
# SESSION_TIMEOUT = 300  # 5 minutes

# # ------------------------ REGISTER ------------------------
# @auth_bp.route("/register", methods=["POST"])
# def register():
#     data = request.json
#     name = data.get("name")
#     email = data.get("email")
#     password = data.get("password")
#     role = data.get("role", "user")

#     conn = get_db_connection()
#     cur = conn.cursor()

#     # check if email exists
#     cur.execute("SELECT * FROM users WHERE email = ?", (email,))
#     if cur.fetchone():
#         conn.close()
#         return jsonify({"status": "error", "message": "Email already exists"}), 400

#     hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
#     cur.execute(
#         """
#         INSERT INTO users (name, email, password_hash, role, created_at)
#         VALUES (?, ?, ?, ?, datetime('now'))
#         """,
#         (name, email, hashed_pw.decode("utf-8"), role),
#     )
#     conn.commit()
#     conn.close()
#     return jsonify({"status": "success", "message": "User registered successfully"}), 200

# # ------------------------ LOGIN ------------------------
# @auth_bp.route("/login", methods=["POST"])
# def login():
#     data = request.json
#     email = data.get("email")
#     password = data.get("password")

#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM users WHERE email = ?", (email,))
#     user = cur.fetchone()
#     conn.close()

#     if not user:
#         return jsonify({"status": "error", "message": "Invalid email"}), 400

#     if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
#         return jsonify({"status": "error", "message": "Incorrect password"}), 400

#     # create session
#     session["user_id"] = user["user_id"]
#     session["role"] = user["role"]
#     session["last_active"] = time.time()

#     return jsonify({
#         "status": "success",
#         "message": "Login successful",
#         "role": user["role"],
#         "name": user["name"]
#     }), 200

# # ------------------------ LOGOUT ------------------------
# @auth_bp.route("/logout", methods=["POST"])
# def logout_user():
#     session.clear()
#     return jsonify({"status": "success", "message": "Logged out"}), 200

# # ------------------------ SESSION CHECK ------------------------
# @auth_bp.route("/check-session", methods=["GET"])
# def check_session():
#     if "user_id" not in session:
#         return jsonify({"logged_in": False}), 200

#     if time.time() - session.get("last_active", 0) > SESSION_TIMEOUT:
#         session.clear()
#         return jsonify({"logged_in": False, "message": "Session expired"}), 200

#     session["last_active"] = time.time()
#     return jsonify({
#         "logged_in": True,
#         "user_id": session["user_id"],
#         "role": session["role"],
#         "name": session.get("name", "")  # optional
#     })

from flask import Blueprint, request, jsonify, session
import bcrypt, time
from utils.database import get_db_connection

auth_bp = Blueprint("auth_bp", __name__)
SESSION_TIMEOUT = 300  # 5 minutes

# ---------------- REGISTER ----------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    if cur.fetchone():
        conn.close()
        return jsonify({"status": "error", "message": "Email already exists"}), 400

    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    cur.execute(
        """INSERT INTO users (name, email, password_hash, role, created_at)
           VALUES (?, ?, ?, ?, datetime('now'))""",
        (name, email, hashed_pw.decode("utf-8"), role)
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "User registered successfully"}), 200

# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    conn.close()

    if not user:
        return jsonify({"status": "error", "message": "Invalid email"}), 400
    if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        return jsonify({"status": "error", "message": "Incorrect password"}), 400

    # ✅ Create session
    session["user_id"] = user["user_id"]
    session["role"] = user["role"]
    session["name"] = user["name"]
    session["last_active"] = time.time()

    return jsonify({"status": "success", "message": "Login successful"}), 200

# ---------------- LOGOUT ----------------
@auth_bp.route("/logout", methods=["POST"])
def logout_user():
    session.clear()
    return jsonify({"status": "success", "message": "Logged out"}), 200

# ---------------- SESSION CHECK ----------------
@auth_bp.route("/check-session", methods=["GET"])
def check_session():
    if "user_id" not in session:
        return jsonify({"logged_in": False}), 200
    if time.time() - session.get("last_active", 0) > SESSION_TIMEOUT:
        session.clear()
        return jsonify({"logged_in": False, "message": "Session expired"}), 200
    session["last_active"] = time.time()
    return jsonify({
        "logged_in": True,
        "user_id": session["user_id"],
        "role": session["role"],
        "name": session.get("name", "")
    })
