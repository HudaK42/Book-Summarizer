# import streamlit as st
# import requests
# import pandas as pd

# # Backend base URL (IMPORTANT: no duplicate /admin)
# BACKEND_URL = "http://127.0.0.1:5000/admin"

# def admin_dashboard():
#     st.title("🛠 Admin Dashboard")

#     # Session object created during login
#     session = st.session_state.get("session_obj")

#     if session is None:
#         st.error("Session expired. Please login again.")
#         st.stop()

#     # ================== ANALYTICS ==================
#     st.subheader("📊 Analytics")

#     res = session.get(f"{BACKEND_URL}/analytics")

#     if res.status_code != 200:
#         st.error(f"Analytics API failed ({res.status_code})")
#         st.text(res.text)
#         st.stop()

#     analytics = res.json()

#     col1, col2 = st.columns(2)
#     col1.metric("Total Summaries", analytics.get("total_summaries", 0))
#     col2.metric(
#         "Avg Summary Length (words)",
#         analytics.get("avg_summary_length", 0),
#     )

#     st.subheader("👤 Most Active Users")
#     if analytics.get("most_active_users"):
#         st.table(pd.DataFrame(analytics["most_active_users"]))
#     else:
#         st.info("No user activity found")

#     st.subheader("📚 Most Summarized Books")
#     if analytics.get("most_summarized_books"):
#         st.table(pd.DataFrame(analytics["most_summarized_books"]))
#     else:
#         st.info("No book data found")

#     # ================== MODERATION ==================
#     st.subheader("🚨 Summary Moderation")

#     res = session.get(f"{BACKEND_URL}/summaries")

#     if res.status_code != 200:
#         st.error("Failed to load summaries")
#         st.text(res.text)
#         st.stop()

#     summaries = res.json().get("summaries", [])

#     if not summaries:
#         st.info("No summaries found")
#         return

#     df = pd.DataFrame(summaries)
#     st.dataframe(df, use_container_width=True)

#     # ================== DELETE SUMMARY ==================
#     st.markdown("### ❌ Delete a Summary")

#     summary_id = st.number_input(
#         "Summary ID",
#         min_value=1,
#         step=1,
#         format="%d"
#     )

#     if st.button("Delete Summary"):
#         del_res = session.delete(
#             f"{BACKEND_URL}/delete-summary/{summary_id}"
#         )

#         if del_res.status_code == 200:
#             st.success("Summary deleted successfully")
#             st.rerun()
#         else:
#             st.error("Failed to delete summary")
#             st.text(del_res.text)

import streamlit as st
import pandas as pd

BACKEND_URL = "http://127.0.0.1:5000/admin"
AUTH_URL = "http://127.0.0.1:5000/auth"


def admin_dashboard():
    st.title("🛠 Admin Dashboard")

    # 🔐 Validate session & role
    if (
        "session_obj" not in st.session_state
        or not st.session_state.get("logged_in")
        or st.session_state.get("role") != "admin"
    ):
        st.error("Unauthorized access. Please login as admin.")
        st.stop()

    session = st.session_state.session_obj

    # ================= LOGOUT =================
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🚪 Logout"):
            try:
                session.post(f"{AUTH_URL}/logout")
            except Exception:
                pass

            # Clear Streamlit session
            st.session_state.clear()
            st.rerun()

    # ================= ANALYTICS =================
    st.subheader("📊 Analytics")

    res = session.get(f"{BACKEND_URL}/analytics")

    if res.status_code != 200:
        st.error("Analytics API failed")
        st.text(res.text)
        st.stop()

    analytics = res.json()

    col1, col2 = st.columns(2)
    col1.metric("Total Summaries", analytics.get("total_summaries", 0))
    col2.metric(
        "Avg Summary Length (words)",
        analytics.get("avg_summary_length", 0),
    )

    st.subheader("👤 Most Active Users")
    st.table(pd.DataFrame(analytics.get("most_active_users", [])))

    st.subheader("📚 Most Summarized Books")
    st.table(pd.DataFrame(analytics.get("most_summarized_books", [])))

    # ================= MODERATION =================
    st.subheader("🚨 Summary Moderation")

    res = session.get(f"{BACKEND_URL}/summaries")

    if res.status_code != 200:
        st.error("Failed to load summaries")
        st.text(res.text)
        st.stop()

    summaries = res.json().get("summaries", [])

    if not summaries:
        st.info("No summaries found")
        return

    df = pd.DataFrame(summaries)
    st.dataframe(df, use_container_width=True)

    # ================= DELETE =================
    st.markdown("### ❌ Delete Summary")

    summary_id = st.number_input(
        "Summary ID",
        min_value=1,
        step=1
    )

    if st.button("Delete Summary"):
        del_res = session.delete(
            f"{BACKEND_URL}/delete-summary/{summary_id}"
        )

        if del_res.status_code == 200:
            st.success("Summary deleted successfully")
            st.rerun()
        else:
            st.error("Delete failed")
            st.text(del_res.text)
