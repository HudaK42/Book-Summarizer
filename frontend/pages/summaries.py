'''
import streamlit as st

BACKEND_URL = "http://127.0.0.1:5000"


# -------------------------------------------------
# LOAD SAVED SUMMARIES
# -------------------------------------------------
def load_summaries(book_id):
    try:
        res = st.session_state.session_obj.get(
            f"{BACKEND_URL}/summaries/book/{book_id}"
        )
        if res.status_code == 200:
            return res.json().get("summaries", [])
        return []
    except Exception:
        return []


# -------------------------------------------------
# MAIN PAGE
# -------------------------------------------------
def summaries_page():
    st.title("🧠 Summary Generator")

    # ---------------- SESSION CHECK ----------------
    try:
        res = st.session_state.session_obj.get(
            f"{BACKEND_URL}/auth/check-session", timeout=5
        )
        if not res.json().get("logged_in"):
            st.warning("Please login first")
            return
    except Exception:
        st.warning("Please login first")
        return

    # ---------------- BOOK CONTEXT ----------------
    selected_book_id = st.session_state.get("selected_book_id")

    # ---------------- INPUT METHOD ----------------
    st.subheader("📌 Choose Input Method")

    input_mode = st.radio(
        "Select one option:",
        ["Select Uploaded Book", "Paste New Text"],
        horizontal=True
    )

    text_input = None

    # ---------------- OPTION 1: SELECT BOOK ----------------
    if input_mode == "Select Uploaded Book":
        try:
            books_res = st.session_state.session_obj.get(
                f"{BACKEND_URL}/books/paginated?page_no=1&limit=50"
            )
            books = books_res.json()

            if not books:
                st.info("No uploaded books found.")
                return

            book_map = {
                f"{b['title']} (ID: {b['book_id']})": b["book_id"]
                for b in books
            }

            selected_label = st.selectbox(
                "📚 Select a book",
                book_map.keys()
            )
            selected_book_id = book_map[selected_label]
            st.session_state.selected_book_id = selected_book_id

        except Exception:
            st.error("Failed to load books")
            return

    # ---------------- OPTION 2: PASTE TEXT ----------------
    else:
        text_input = st.text_area(
            "📄 Paste text here",
            height=300,
            placeholder="Paste book content or any long text..."
        )

    # ---------------- SUMMARY OPTIONS ----------------
    st.subheader("⚙️ Summary Options")

    col1, col2, col3 = st.columns(3)

    with col1:
        summary_length = st.selectbox(
            "Summary Length",
            ["short", "medium", "long"]
        )

    with col2:
        summary_style = st.selectbox(
            "Summary Style",
            ["paragraphs", "bullets"]
        )

    with col3:
        detail_level = st.selectbox(
            "Detail Level",
            ["concise", "detailed"]
        )

    # ---------------- GENERATE SUMMARY ----------------
    st.markdown("---")

    if st.button("🚀 Generate Summary", use_container_width=True):

        if input_mode == "Paste New Text" and not text_input.strip():
            st.error("Please paste some text")
            return

        payload = {
            "summary_length": summary_length,
            "summary_style": summary_style,
            "detail_level": detail_level
        }

        if input_mode == "Select Uploaded Book":
            payload["book_id"] = st.session_state.selected_book_id
        else:
            payload["text"] = text_input

        with st.spinner("⏳ Generating summary..."):
            try:
                res = st.session_state.session_obj.post(
                    f"{BACKEND_URL}/summarize",
                    json=payload,
                    timeout=300
                )
                data = res.json()

                if res.status_code != 200 or data.get("status") != "success":
                    st.error(data.get("error", "Summary generation failed"))
                    return

            except Exception:
                st.error("Backend error")
                return

        # ---------------- DISPLAY GENERATED SUMMARY ----------------
        st.success("✅ Summary Generated Successfully")

        st.subheader("📑 Generated Summary")
        st.write(data["summary"])

        st.caption(
            f"⏱ Processing Time: {data.get('processing_time', '-')} seconds | "
            f"📦 Chunks Used: {data.get('total_chunks', '-')}"
        )

        # Refresh saved summaries after generation
        st.rerun()

    # =================================================
    # SAVED SUMMARIES SECTION
    # =================================================
    st.markdown("## 📂 Your Saved Summaries")

    if not st.session_state.get("selected_book_id"):
        st.info("Select a book to view its saved summaries")
        return

    summaries = load_summaries(st.session_state.selected_book_id)

    if not summaries:
        st.info("No summaries found for this book")
        return

    for s in summaries:
        # ---------------- DISPLAY SUMMARY ----------------
        with st.expander(f"📝 Summary ID: {s['summary_id']} | Version {s['version']}"):
            st.write(s["summary_text"])

            # ---------------- EDIT ----------------
            edited_text = st.text_area(
                "✏️ Edit Summary",
                value=s["summary_text"],
                height=200,
                key=f"edit_{s['summary_id']}"
            )

            if st.button("🔄 Update Summary", key=f"update_{s['summary_id']}"):
                try:
                    res = st.session_state.session_obj.put(
                        f"{BACKEND_URL}/summaries/{s['summary_id']}",
                        json={"summary_text": edited_text}
                    )
                    if res.status_code == 200:
                        st.success("Summary updated ✅")
                        st.rerun()
                    else:
                        st.error("Update failed")
                except Exception:
                    st.error("Backend error")

            # ---------------- DELETE ----------------
            if st.button("🗑 Delete Summary", key=f"del_{s['summary_id']}"):
                try:
                    res = st.session_state.session_obj.delete(
                        f"{BACKEND_URL}/summaries/{s['summary_id']}"
                    )
                    if res.status_code == 200:
                        st.success("Summary deleted ✅")
                        st.rerun()
                    else:
                        st.error("Delete failed")
                except Exception:
                    st.error("Backend error")
'''

import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000"

# -------------------------------
# Load summaries for selected book
# -------------------------------
def load_summaries(book_id):
    try:
        res = st.session_state.session_obj.get(
            f"{BACKEND_URL}/summaries/book/{book_id}"
        )
        if res.status_code == 200:
            return res.json().get("summaries", [])
        return []
    except Exception:
        return []


# -------------------------------
# Summaries Page
# -------------------------------
def summaries_page():
    st.title("🧠 Summary Generator")

    # ---------------- SESSION CHECK ----------------
    try:
        res = st.session_state.session_obj.get(
            f"{BACKEND_URL}/auth/check-session", timeout=5
        )
        if not res.json().get("logged_in"):
            st.warning("Please login first")
            return
    except Exception:
        st.warning("Please login first")
        return

    # ---------------- SELECT BOOK ----------------
    selected_book_id = st.session_state.get("selected_book_id")
    text_input = None

    input_mode = st.radio(
        "Select Input Method:",
        ["Select Uploaded Book", "Paste New Text"],
        horizontal=True
    )

    if input_mode == "Select Uploaded Book":
        try:
            books_res = st.session_state.session_obj.get(
                f"{BACKEND_URL}/books/paginated?page_no=1&limit=50"
            )
            books = books_res.json()
            if not books:
                st.info("No uploaded books found.")
                return

            book_map = {f"{b['title']} (ID: {b['book_id']})": b["book_id"] for b in books}
            selected_label = st.selectbox("📚 Select a book", book_map.keys())
            selected_book_id = book_map[selected_label]
            st.session_state.selected_book_id = selected_book_id
        except Exception:
            st.error("Failed to load books")
            return

    else:
        text_input = st.text_area(
            "📄 Paste text here",
            height=300,
            placeholder="Paste book content or any long text..."
        )

    # ---------------- SUMMARY OPTIONS ----------------
    st.subheader("⚙️ Summary Options")
    col1, col2, col3 = st.columns(3)
    with col1:
        summary_length = st.selectbox("Summary Length", ["short", "medium", "long"])
    with col2:
        summary_style = st.selectbox("Summary Style", ["paragraphs", "bullets"])
    with col3:
        detail_level = st.selectbox("Detail Level", ["concise", "detailed"])

    # ---------------- GENERATE SUMMARY ----------------
    if st.button("🚀 Generate Summary", use_container_width=True):
        if input_mode == "Paste New Text" and not text_input.strip():
            st.error("Please paste some text")
            return

        payload = {"summary_length": summary_length,
                   "summary_style": summary_style,
                   "detail_level": detail_level}

        if input_mode == "Select Uploaded Book":
            payload["book_id"] = selected_book_id
        else:
            payload["text"] = text_input

        with st.spinner("⏳ Generating summary..."):
            try:
                res = st.session_state.session_obj.post(
                    f"{BACKEND_URL}/summarize", json=payload, timeout=300
                )
                data = res.json()
                if res.status_code != 200 or data.get("status") != "success":
                    st.error(data.get("error", "Summary generation failed"))
                    return
            except Exception:
                st.error("Backend error")
                return

        st.success("✅ Summary Generated Successfully")
        st.subheader("📑 Generated Summary")
        st.write(data["summary"])
        st.caption(
            f"⏱ Processing Time: {data.get('processing_time', '-')}"
            f" seconds | 📦 Chunks Used: {data.get('total_chunks', '-')}"
        )
        st.rerun()  # refresh saved summaries

    # ---------------- SAVED SUMMARIES ----------------
    st.markdown("## 📂 Your Saved Summaries")

    if not selected_book_id:
        st.info("Select a book to view saved summaries")
        return

    summaries = load_summaries(selected_book_id)

    if not summaries:
        st.info("No summaries found for this book")
        return

    

    for s in summaries:
        with st.expander(f"📝 Summary ID: {s['summary_id']} | Version {s['version']}"):
            st.write(s["summary_text"])

        # ---------------- EDIT ----------------
            edited_text = st.text_area(
                "✏️ Edit Summary",
                value=s["summary_text"],
                height=200,
                key=f"edit_{s['summary_id']}"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("🔄 Update Summary", key=f"update_{s['summary_id']}"):
                    try:
                        res = st.session_state.session_obj.put(
                            f"{BACKEND_URL}/summaries/{s['summary_id']}",
                            json={"summary_text": edited_text}
                        )
                        if res.status_code == 200:
                            st.success("Summary updated ✅")
                            st.rerun()
                        else:
                            st.error("Update failed")
                    except Exception:
                        st.error("Backend error")

            with col2:
                if st.button("🗑 Delete Summary", key=f"del_{s['summary_id']}"):
                    try:
                        res = st.session_state.session_obj.delete(
                            f"{BACKEND_URL}/summaries/{s['summary_id']}"
                        )
                        if res.status_code == 200:
                            st.success("Summary deleted ✅")
                            st.rerun()
                        else:
                            st.error("Delete failed")
                    except Exception:
                        st.error("Backend error")
