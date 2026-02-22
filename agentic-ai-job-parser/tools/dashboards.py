import streamlit as st
from job_search_tool import fetch_jobs

st.set_page_config(page_title="AI Job Dashboard", layout="wide")
st.title("AI Job Search Dashboard")

# --- Inputs ---
query = st.text_input("Job title or keywords", "Data Scientist")
location = st.text_input("Location", "United States")
num_jobs = st.slider("Number of jobs to fetch", min_value=1, max_value=20, value=10)

# --- Session state for persistence ---
if "jobs" not in st.session_state:
    st.session_state.jobs = []

if st.button("Fetch Jobs"):
    st.session_state.jobs = fetch_jobs(query=query, location=location, num_pages=1)

# --- Display cards ---
for idx, job in enumerate(st.session_state.jobs):
    with st.container():
        st.markdown(f"""
        <div style='background-color:#f9fafb; padding:20px; border-radius:12px; margin-bottom:15px; box-shadow:0 4px 8px rgba(0,0,0,0.08)'>
            <div style='font-size:20px; font-weight:bold; color:#1f2937'>{job['title']}</div>
            <div style='font-size:16px; color:#4b5563'>{job['company']}</div>
            <div style='font-size:14px; color:#6b7280'>
                Location: {job.get("job_location", "N/A")} | Posted: {job.get("date_posted")} | Type: {job.get("job_employment_type_text","N/A")}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Buttons
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            if st.button(f"Tailor Resume {idx}"):
                st.success(f"Tailored Resume ready for {job['title']} at {job['company']}")

        with col2:
            if st.button(f"Generate Cover Letter {idx}"):
                st.success(f"Cover Letter ready for {job['title']} at {job['company']}")

        with col3:
            st.markdown(f"[Apply Here]({job['link']})", unsafe_allow_html=True)