import sqlite3
import json
from datetime import datetime

DB_PATH = "data/app.db"

# ---------------- CONNECTION ----------------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # so you can access columns by name
    return conn

# ---------------- USERS ----------------
def create_user(name, email, password_hash, role="user"):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (name, email, password_hash, role)
        VALUES (?, ?, ?, ?)
    """, (name, email, password_hash, role))
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    conn.close()
    return user

# ---------------- BOOKS ----------------
def create_book(user_id, title, author, chapter, file_path, raw_text):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO books (user_id, title, author, chapter, file_path, raw_text)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, title, author, chapter, file_path, raw_text))
    conn.commit()
    conn.close()

def update_book_status(book_id, status):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE books SET status = ? WHERE book_id = ?", (status, book_id))
    conn.commit()
    conn.close()

# ---------------- SUMMARIES ----------------
def create_summary(book_id, user_id, summary_text, length, style, chunk_summaries, processing_time):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO summaries 
        (book_id, user_id, summary_text, summary_length, summary_style, chunk_summaries, processing_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (book_id, user_id, summary_text, length, style, json.dumps(chunk_summaries), processing_time))
    conn.commit()
    conn.close()

def get_summaries_by_user(user_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM summaries WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows
