import streamlit as st

def intro_page():
    st.set_page_config(page_title="AI Book Summarizer", layout="wide")

    st.markdown(
        """
        <style>
        body {
            background-image: url("https://images.unsplash.com/photo-1524995997946-a1c2e315a42f");
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("📘 AI Book Summarizer")
    st.subheader("Turn your books into smart summaries instantly")

    st.write("""
    Upload books or paste text and generate concise summaries using AI.
    Supports PDF, DOCX, and TXT files.
    """)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Login"):
            st.session_state.page = "login"
    with col2:
        if st.button("📝 Register"):
            st.session_state.page = "register"
