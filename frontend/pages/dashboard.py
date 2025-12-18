import streamlit as st
from pages import upload, my_books, summaries
import requests

BACKEND_URL = "http://127.0.0.1:5000"

def dashboard_page():

    # 🔐 ALWAYS VERIFY FLASK SESSION
    try:
        res = st.session_state.session_obj.get(
            f"{BACKEND_URL}/auth/check-session",
            timeout=5
        )
        data = res.json()
        if not data.get("logged_in"):
            st.warning("Please login first!")
            st.session_state.page = "login"
            st.rerun()
    except Exception:
        st.warning("Please login first!")
        st.session_state.page = "login"
        st.rerun()

    # ---------------- SIDEBAR ----------------
    st.sidebar.title("📚 Navigation")

    choice = st.sidebar.radio(
        "Go to",
        ["Upload", "My Books", "Summaries", "Logout"]
    )

    if choice == "Upload":
        upload.upload_page()

    elif choice == "My Books":
        my_books.my_books_page()

    elif choice == "Summaries":
        summaries.summaries_page()

    else:  # 🚪 LOGOUT
        st.session_state.session_obj.post(f"{BACKEND_URL}/auth/logout")
        st.session_state.clear()
        st.session_state.page = "intro"
        st.rerun()
