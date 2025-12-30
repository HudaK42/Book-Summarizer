

# import streamlit as st

# BACKEND_URL = "http://127.0.0.1:5000"

# def upload_page():
#     st.header("📤 Upload Book or Text")
#     st.info("Maximum upload size: 10 MB")

#     mode = st.radio("Choose Input Type", ["Upload File", "Paste Text"])

#     title = st.text_input("Title")
#     author = st.text_input("Author")
#     chapter = st.text_input("Chapter")

#     if mode == "Upload File":
#         file = st.file_uploader("Upload PDF/DOCX/TXT", type=["pdf", "docx", "txt"])

#         if st.button("Upload"):
#             if not file:
#                 st.error("No file selected")
#                 return

#             res = st.session_state.session_obj.post(
#                 f"{BACKEND_URL}/upload_file",
#                 files={"file": file},
#                 data={"title": title, "author": author, "chapter": chapter},
#                 timeout=20
#             )

#             try:
#                 response = res.json()
#             except Exception:
#                 st.error("Invalid response from server")
#                 return

#             if res.status_code == 200:
#                 st.success(response.get("message", "Upload successful"))
#             else:
#                 st.error(response.get("error", "Upload failed"))

#     else:
#         text = st.text_area("Paste Text", height=300)

#         if st.button("Submit"):
#             if not text.strip():
#                 st.error("Text cannot be empty")
#                 return

#             res = st.session_state.session_obj.post(
#                 f"{BACKEND_URL}/submit_text",
#                 json={
#                     "title": title,
#                     "author": author,
#                     "chapter": chapter,
#                     "text": text
#                 },
#                 timeout=20
#             )

#             try:
#                 response = res.json()
#             except Exception:
#                 st.error("Invalid response from server")
#                 return

#             if res.status_code == 200:
#                 st.success(response.get("message", "Text submitted successfully"))
#             else:
#                 st.error(response.get("error", "Submission failed"))


import streamlit as st

BACKEND_URL = "http://127.0.0.1:5000"

def upload_page():
    st.header("📤 Upload Book or Text")
    st.info("Maximum upload size: 10 MB")

    mode = st.radio("Choose Input Type", ["Upload File", "Paste Text"])

    title = st.text_input("Title")
    author = st.text_input("Author")
    chapter = st.text_input("Chapter")

    # ---------------- Upload File ----------------
    if mode == "Upload File":
        file = st.file_uploader("Upload PDF/DOCX/TXT", type=["pdf", "docx", "txt"])

        if st.button("Upload"):
            if not file:
                st.error("No file selected")
                return

            data = {
                "title": title,
                "author": author,
                "chapter": chapter
            }

            

            files = {
                "file": (file.name, file.getvalue(), file.type)
            }

            res = st.session_state.session_obj.post(
                f"{BACKEND_URL}/upload_file",
                files=files,
                data={
                    "title": title.strip(),
                    "author": author.strip(),
                    "chapter": chapter.strip()
                },
                timeout=120
            )


            try:
                response = res.json()
            except Exception:
                st.error(f"Backend returned invalid response:\n{res.text}")
                return

            if res.status_code == 200 and response.get("status") == "success":
                st.success(response.get("message", "Upload successful"))
                ## additional info
                st.write("Language:", response.get("language", "-"))
                st.write("Total Chunks:", response.get("total_chunks", "-"))
            else:
                st.error(response.get("message", "Upload failed"))

    # ---------------- Paste Text ----------------
    else:
        text = st.text_area("Paste Text", height=300)

        if st.button("Submit"):
            if not text.strip():
                st.error("Text cannot be empty")
                return

            payload = {
                "title": title,
                "author": author,
                "chapter": chapter,
                "text": text
            }

            res = st.session_state.session_obj.post(
                f"{BACKEND_URL}/submit_text",
                json=payload,
                timeout=120
            )

            try:
                response = res.json()
            except Exception:
                st.error(f"Backend returned invalid response:\n{res.text}")
                return

            if res.status_code == 200 and response.get("status") == "success":
                st.success(response.get("message", "Text submitted successfully"))
                ## additional info
                st.write("Language:", response.get("language", "-"))
                st.write("Total Chunks:", response.get("total_chunks", "-"))
            else:
                st.error(response.get("message", "Submission failed"))
