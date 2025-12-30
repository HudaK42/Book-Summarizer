#frontend/app.py
import streamlit as st
import requests
from pages import intro, dashboard
from pages import admin_dashboard


import auth

BACKEND_URL = "http://127.0.0.1:5000"




def init_session_state():
    defaults = {
        "page": "intro",
        "logged_in": False,
        "user_id": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session_state()

st.set_page_config(page_title="AI Book Summarizer", layout="wide")

# ---------------- SESSION ----------------
if "session_obj" not in st.session_state:
    st.session_state.session_obj = requests.Session()

if "page" not in st.session_state:
    st.session_state.page = "intro"

# ---------------- CHECK FLASK SESSION ----------------
def is_logged_in():
    try:
        res = st.session_state.session_obj.get(
            f"{BACKEND_URL}/auth/check-session",
            timeout=5
        )
        return res.json().get("logged_in", False)
    except:
        return False

# # ---------------- ROUTING ----------------
# if is_logged_in():
#     dashboard.dashboard_page()
# elif st.session_state.page in ["login", "register"]:
#     auth.auth_page()
# else:
#     intro.intro_page()


# ---------------- ROUTING ----------------
if is_logged_in():
    role = st.session_state.get("role")

    if role == "admin":
        from pages import admin_dashboard
        admin_dashboard.admin_dashboard()
    else:
        dashboard.dashboard_page()

elif st.session_state.page in ["login", "register"]:
    auth.auth_page()
else:
    intro.intro_page()
