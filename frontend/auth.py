

# import streamlit as st
# import requests, re

# BACKEND_URL = "http://127.0.0.1:5000/auth"

# # ---------------- Helpers ----------------
# def valid_email(email):
#     return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)

# def valid_password(password):
#     return len(password) == 8

# # ---------------- Session object ----------------
# if "session_obj" not in st.session_state:
#     st.session_state.session_obj = requests.Session()

# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# def auth_page():
#     page = st.session_state.get("page", "login")
#     if page == "login":
#         login()
#     else:
#         register()

# def login():
#     st.title("🔐 Login")
#     with st.form("login_form"):
#         email = st.text_input("Email")
#         password = st.text_input("Password", type="password")
#         login_btn = st.form_submit_button("Login")

#     if login_btn:
#         try:
#             res = st.session_state.session_obj.post(
#                 f"{BACKEND_URL}/login",
#                 json={"email": email, "password": password},
#                 timeout=60
#             )
#             data = res.json()

#             if res.status_code == 200 and data.get("status") == "success":
#                 st.success("Login successful")
#                 st.session_state.logged_in = True
#                 st.session_state.page = "dashboard"

#                 # Optional: fetch session info immediately
#                 session_res = st.session_state.session_obj.get(f"{BACKEND_URL}/check-session")
#                 session_data = session_res.json()
#                 st.session_state.user_id = session_data.get("user_id")
#                 st.session_state.user_name = session_data.get("name")
#                 st.rerun()

#             else:
#                 st.error(data.get("message"))

#         except Exception as e:
#             st.error(f"Error connecting to backend: {e}")


# def register():
#     st.title("📝 Register")
#     with st.form("register_form"):
#         name = st.text_input("Full Name", key="reg_name")
#         email = st.text_input("Email", key="reg_email")
#         password = st.text_input("Password", type="password", key="reg_password")
#         confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
#         role = st.selectbox("Role", ["user", "admin"], key="reg_role")
#         register_btn = st.form_submit_button("Register")

#     if register_btn:
#         if not valid_email(email):
#             st.error("Invalid email")
#             return
#         if not valid_password(password):
#             st.error("Password must be 8 characters")
#             return
#         if password != confirm:
#             st.error("Passwords do not match")
#             return
#         try:
#             res = st.session_state.session_obj.post(
#                 f"{BACKEND_URL}/register",
#                 json={"name": name, "email": email, "password": password, "role": role},
#                 timeout=60
#             )
#             data = res.json()
#             if data.get("status") == "success":
#                 st.success("Registration successful! Please login now.")
#                 st.session_state.page = "login"
#                 st.rerun()
#             else:
#                 st.error(data.get("message"))
#         except Exception as e:
#             st.error(f"Error connecting to backend: {e}")

import streamlit as st
import requests
import re

BACKEND_URL = "http://127.0.0.1:5000/auth"

# ---------------- Helpers ----------------
def valid_email(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)

def valid_password(password):
    return len(password) == 8


# ---------------- Session Initialization ----------------
if "session_obj" not in st.session_state:
    st.session_state.session_obj = requests.Session()  # ✅ MUST be Session

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"


# ---------------- Router ----------------
def auth_page():
    if st.session_state.page == "login":
        login()
    else:
        register()


# ---------------- Login ----------------
def login():
    st.title("🔐 Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

    if not login_btn:
        return

    try:
        res = st.session_state.session_obj.post(
            f"{BACKEND_URL}/login",
            json={"email": email, "password": password},
            timeout=30
        )

        if res.status_code != 200:
            st.error("Invalid login credentials")
            return

        data = res.json()

        if data.get("status") != "success":
            st.error(data.get("message", "Login failed"))
            return

        # ---------------- SUCCESS ----------------
        st.success("Login successful")
        st.session_state.logged_in = True

        # ---------------- Fetch session info ----------------
        session_res = st.session_state.session_obj.get(
            f"{BACKEND_URL}/check-session",
            timeout=30
        )

        if session_res.status_code != 200:
            st.error("Session verification failed")
            return

        session_data = session_res.json()

        st.session_state.user_id = session_data.get("user_id")
        st.session_state.user_name = session_data.get("name")
        st.session_state.role = session_data.get("role")

        # ---------------- Role Redirect ----------------
        if st.session_state.role == "admin":
            st.session_state.page = "admin_dashboard"
        else:
            st.session_state.page = "dashboard"

        st.rerun()

    except requests.exceptions.RequestException as e:
        st.error(f"Backend connection error: {e}")


# ---------------- Register ----------------
def register():
    st.title("📝 Register")

    with st.form("register_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        role = st.selectbox("Role", ["user", "admin"])
        register_btn = st.form_submit_button("Register")

    if not register_btn:
        return

    # ---------------- Validation ----------------
    if not valid_email(email):
        st.error("Invalid email format")
        return

    if not valid_password(password):
        st.error("Password must be exactly 8 characters")
        return

    if password != confirm:
        st.error("Passwords do not match")
        return

    try:
        res = st.session_state.session_obj.post(
            f"{BACKEND_URL}/register",
            json={
                "name": name,
                "email": email,
                "password": password,
                "role": role
            },
            timeout=30
        )

        if res.status_code != 200:
            st.error("Registration failed")
            return

        data = res.json()

        if data.get("status") == "success":
            st.success("Registration successful! Please login.")
            st.session_state.page = "login"
            st.rerun()
        else:
            st.error(data.get("message", "Registration error"))

    except requests.exceptions.RequestException as e:
        st.error(f"Backend connection error: {e}")
