# import streamlit as st
# import pandas as pd
# import requests

# BACKEND_URL = "http://127.0.0.1:5000"

# def my_books_page():
#     st.header("📚 My Books")

#     search = st.text_input("Search by title or author")
#     sort = st.selectbox("Sort by", ["newest", "oldest"])

#     res = st.session_state.session_obj.get(
#     f"{BACKEND_URL}/books",
#     params={"q": search, "sort": sort},
#     timeout=10
# )
#     books = res.json().get("books", [])


#     if not books:
#         st.info("No books found")
#         return

#     df = pd.DataFrame(books)
#     st.dataframe(df)


# import streamlit as st
# import pandas as pd
# import requests

# BACKEND_URL = "http://127.0.0.1:5000"

# def my_books_page():
#     st.header("📚 My Books")

#     # ---------------- UI CONTROLS ----------------
#     search_text = st.text_input("🔍 Search by title or author")

#     col1, col2 = st.columns(2)

#     with col1:
#         sort_option = st.selectbox(
#             "Sort by",
#             ["newest", "oldest", "alphabetical"]
#         )

#     with col2:
#         filter_option = st.selectbox(
#             "Filter by status",
#             ["all", "uploaded", "completed"]
#         )

#     # Pagination state
#     if "book_page" not in st.session_state:
#         st.session_state.book_page = 1

#     # ---------------- API CALL ----------------
#     params = {
#         "q": search_text,
#         "sort": sort_option,
#         "status": filter_option,
#         "page": st.session_state.book_page,
#         "limit": 5
#     }

#     res = st.session_state.session_obj.get(
#         f"{BACKEND_URL}/books",
#         params=params,
#         timeout=10
#     )

#     try:
#         data = res.json()
#     except Exception:
#         st.error("Backend error")
#         return

#     books = data.get("books", [])
    
#     total = data.get("total", 0)

#     if not books:
#         st.info("No books found")
#         return

#     # ---------------- DISPLAY ----------------
#     df = pd.DataFrame(books)
#     df = df[["title", "author", "uploaded_at", "status"]]

#     st.dataframe(df, use_container_width=True)

#     # ---------------- ACTION BUTTONS ----------------
#     for book in books:
#         with st.expander(f"📘 {book['title']}"):
#             col1, col2, col3 = st.columns(3)

#             col1.button(
#                 "👁 View",
#                 key=f"view_{book['book_id']}"
#             )

#             col2.button(
#                 "📝 Generate Summary",
#                 key=f"summary_{book['book_id']}"
#             )

#             col3.button(
#                 "🗑 Delete",
#                 key=f"delete_{book['book_id']}"
#             )

#     # ---------------- PAGINATION ----------------
#     col_prev, col_next = st.columns(2)

#     if col_prev.button("⬅ Previous") and st.session_state.book_page > 1:
#         st.session_state.book_page -= 1
#         st.rerun()

#     if col_next.button("Next ➡") and len(books) == 5:
#         st.session_state.book_page += 1
#         st.rerun()


#     if col1.button("👁 View", key=f"view_{book['book_id']}"):
#         res = st.session_state.session_obj.get(
#             f"{BACKEND_URL}/books/{book['book_id']}"
#     )
#         st.json(res.json())


#     if col2.button("📝 Generate Summary", key=f"summary_{book['book_id']}"):
#         st.session_state.session_obj.post(
#             f"{BACKEND_URL}/books/{book['book_id']}/summarize"
#     )
#         st.success("Summarization started")


#     if col3.button("🗑 Delete", key=f"delete_{book['book_id']}"):
#         st.session_state.session_obj.delete(
#             f"{BACKEND_URL}/books/{book['book_id']}"
#     )
#         st.success("Book deleted")
#         st.rerun()


# import streamlit as st
# import requests

# BACKEND_URL = "http://127.0.0.1:5000"

# def my_books_page():
#     st.header("📚 My Books")

#     # -------- Controls --------
#     search_text = st.text_input("🔍 Search by title or author")

#     col1, col2, col3 = st.columns(3)
#     sort_option = col1.selectbox(
#         "Sort by",
#         ["newest", "oldest", "az"],
#         format_func=lambda x: {
#             "newest": "Newest",
#             "oldest": "Oldest",
#             "az": "A–Z"
#         }[x]
#     )

#     filter_option = col2.selectbox(
#         "Filter",
#         ["all", "summarized", "not_summarized"]
#     )

#     # -------- Pagination state --------
#     if "page" not in st.session_state:
#         st.session_state.page = 1

#     # -------- Request params --------
#     params = {
#         "q": search_text,
#         "sort": sort_option,
#         "page": st.session_state.page,
#         "limit": 5
#     }

#     if filter_option != "all":
#         params["status"] = filter_option

#     # -------- API Call --------
#     res = st.session_state.session_obj.get(
#         f"{BACKEND_URL}/books",
#         params=params,
#         timeout=60
#     )

#     data = res.json()
#     books = data.get("books", [])
#     total = data.get("total", 0)

#     if not books:
#         st.info("No books found")
#         return

#     # -------- Display Books --------
#     for book in books:
#         st.markdown(f"### 📘 {book['title']}")
#         st.write(f"**Author:** {book.get('author','-')}")
#         st.write(f"**Uploaded:** {book['upload_date']}")
#         st.write(f"**Status:** {book['status']}")

#         a, b, c = st.columns(3)

#         # VIEW
#         if a.button("👁 View", key=f"view_{book['book_id']}"):
#             res = st.session_state.session_obj.get(
#                 f"{BACKEND_URL}/books/{book['book_id']}"
#             )
#             st.json(res.json())

#         # SUMMARIZE
#         if b.button("📝 Summarize", key=f"sum_{book['book_id']}"):
#             st.session_state.session_obj.post(
#                 f"{BACKEND_URL}/books/{book['book_id']}/summarize"
#             )
#             st.success("Summarization started")

#         # DELETE
#         if c.button("🗑 Delete", key=f"del_{book['book_id']}"):
#             st.session_state.session_obj.delete(
#                 f"{BACKEND_URL}/books/{book['book_id']}"
#             )
#             st.success("Book deleted")
#             st.rerun()

#         st.divider()

#     # -------- Pagination Buttons --------
#     total_pages = (total + 4) // 5

#     p1, p2 = st.columns(2)
#     if p1.button("⬅ Previous") and st.session_state.page > 1:
#         st.session_state.page -= 1
#         st.rerun()

#     if p2.button("Next ➡") and st.session_state.page < total_pages:
#         st.session_state.page += 1
#         st.rerun()



import streamlit as st

BACKEND_URL = "http://127.0.0.1:5000"

def my_books_page():
    st.header("📚 My Books")

    if not st.session_state.get("logged_in", False):
        st.warning("Please login to view your books")
        return

    search_text = st.text_input("🔍 Search by title or author")

    col1, col2, col3 = st.columns(3)
    sort_option = col1.selectbox(
        "Sort by",
        ["newest", "oldest", "az"],
        format_func=lambda x: {"newest":"Newest","oldest":"Oldest","az":"A–Z"}[x]
    )

    filter_option = col2.selectbox(
        "Filter",
        ["all", "summarized", "not_summarized"]
    )

    if "page_no" not in st.session_state:
        st.session_state.page_no = 1

    STATUS_MAP = {
        "summarized": "completed",
        "not_summarized": "uploaded"
    }

    params = {
        "q": search_text,
        "sort": sort_option,
        "page_no": st.session_state.page_no,
        "limit": 5
    }

    if filter_option != "all":
        params["status"] = STATUS_MAP[filter_option]

    try:
        res = st.session_state.session_obj.get(
            f"{BACKEND_URL}/books",
            params=params,
            timeout=60
        )

        data = res.json()
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
        return

    books = data.get("books", [])
    total = data.get("total", 0)

    if not books:
        st.info("No books found")
        return

    for book in books:
        st.markdown(f"### 📘 {book['title']}")
        st.write(f"**Author:** {book.get('author','-')}")
        st.write(f"**Uploaded:** {book.get('upload_date','-')}")
        st.write(f"**Status:** {book.get('status','-')}")

        a, b, c = st.columns(3)

        if a.button("👁 View", key=f"view_{book['book_id']}"):
            res = st.session_state.session_obj.get(
                f"{BACKEND_URL}/books/{book['book_id']}"
            )
            st.json(res.json())

        if b.button("📝 Summarize", key=f"sum_{book['book_id']}"):
            st.session_state.session_obj.post(
                f"{BACKEND_URL}/books/{book['book_id']}/summarize"
            )
            st.success("Summarization started")

        if c.button("🗑 Delete", key=f"del_{book['book_id']}"):
            st.session_state.session_obj.delete(
                f"{BACKEND_URL}/books/{book['book_id']}"
            )
            st.success("Book deleted")
            st.rerun()

        st.divider()

    total_pages = (total + 4) // 5

    p1, p2 = st.columns(2)

    if p1.button("⬅ Previous") and st.session_state.page_no > 1:
        st.session_state.page_no -= 1
        st.rerun()

    if p2.button("Next ➡") and st.session_state.page_no < total_pages:
        st.session_state.page_no += 1
        st.rerun()
