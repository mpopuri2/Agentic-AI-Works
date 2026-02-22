import streamlit as st
from tools.job_search_tool import fetch_jobs

st.set_page_config(page_title="AI Job Dashboard", layout="wide")

st.title("🚀 AI Job Search Dashboard")

# Navigation state
if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_job" not in st.session_state:
    st.session_state.selected_job = None

# Inputs
query = st.text_input("Job title", "Data Scientist")
location = st.text_input("Location", "United States")
num_jobs = st.slider("Jobs", 1, 20, 10)

if "jobs" not in st.session_state:
    st.session_state.jobs = []

if st.button("Fetch Jobs"):
    st.session_state.jobs = fetch_jobs(query, location, limit = num_jobs)

st.markdown("---")

# Display Job Cards
for idx, job in enumerate(st.session_state.jobs):

    col_left, col_right = st.columns([4, 1])

    with col_left:
        st.markdown(
            f"""
            <div style="
                background-color:#ffffff;
                padding:18px;
                border-radius:12px;
                margin-bottom:12px;
                box-shadow:0 4px 10px rgba(0,0,0,0.05);
            ">
                <div style="font-size:20px; font-weight:600; color:#111827;">
                    {job['title']}
                </div>
                <div style="font-size:16px; color:#374151;">
                    {job['company']}
                </div>
                <div style="font-size:14px; color:#6b7280;">
                    📍 {job['job_location']}  
                    🕒 {job['date_posted']}  
                    💼 {job['job_type']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_right:
        if st.button("Apply", key=f"apply_{idx}"):
            st.session_state.selected_job = job
            st.session_state.page = "details"
            st.rerun()

        if st.button("Resume", key=f"resume_{idx}"):
            st.success("Resume tailoring started")

        if st.button("Cover", key=f"cover letter_{idx}"):
            st.success("Cover letter generating")

# Navigate to details page
if st.session_state.page == "details":
    st.switch_page("pages/job_details.py")



