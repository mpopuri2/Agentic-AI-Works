import streamlit as st
import random
from utils.job_search_tool import search_jobs

st.set_page_config(layout="wide")

# ----------- CSS Styling -----------

st.markdown("""
<style>

.job-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    margin-bottom: 15px;
}

.job-title {
    font-size: 20px;
    font-weight: 600;
    color: #111827;
}

.job-company {
    font-size: 15px;
    color: #374151;
    margin-top: 4px;
}

.job-meta {
    margin-top: 10px;
    font-size: 13px;
    color: #6b7280;
}

.match-panel {
    background: linear-gradient(135deg, #0f766e, #059669);
    color: white;
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    height: 100%;
}

.apply-btn {
    background-color: #10b981;
    color: white;
    padding: 6px 14px;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 500;
}

</style>
""", unsafe_allow_html=True)

st.title("Recommended Jobs")

query = st.text_input("Search", "Data Scientist United States")
num_jobs = st.slider("Number of jobs", 1, 20, 5)

if st.button("Search Jobs"):
    st.session_state.jobs = search_jobs(query)

# ----------- Display Jobs -----------

if "jobs" in st.session_state:

    jobs = st.session_state.jobs[:num_jobs]

    for idx, job in enumerate(jobs):

        match_score = random.randint(75, 98)

        col_left, col_right = st.columns([4,1])

        # LEFT CARD
        with col_left:
            st.markdown(f"""
            <div class="job-card">
                <div class="job-title">
                    {job.get("job_title","N/A")}
                </div>

                <div class="job-company">
                    {job.get("employer_name","N/A")}
                </div>

                <div class="job-meta">
                    📍 {job.get("job_city","")} {job.get("job_state","")} &nbsp;&nbsp;
                    💼 {job.get("job_employment_type","N/A")} &nbsp;&nbsp;
                    🕒 {job.get("job_posted_at_datetime_utc","Recently")}
                </div>
            </div>
            """, unsafe_allow_html=True)

            b1, b2, b3 = st.columns([1,1,1])

            # Apply button
            apply_link = job.get("job_apply_link") or job.get("job_google_link")

            with b1:
                if apply_link:
                    st.markdown(
                        f'<a href="{apply_link}" target="_blank" class="apply-btn">Apply</a>',
                        unsafe_allow_html=True
                    )

            # Resume
            with b2:
                if st.button("Resume", key=f"resume_{idx}"):
                    st.success("Resume tailored (demo)")

            # Cover Letter
            with b3:
                if st.button("Cover", key=f"cover_{idx}"):
                    st.success("Cover letter generated (demo)")

            # View details
            if st.button("View Details", key=f"details_{idx}"):
                st.session_state.selected_job = job
                st.switch_page("pages/2_Job_Details.py")

        # RIGHT MATCH PANEL
        with col_right:
            st.markdown(f"""
            <div class="match-panel">
                <div style="font-size:32px;font-weight:700;">
                    {match_score}%
                </div>
                <div style="font-size:14px;margin-top:6px;">
                    {"STRONG MATCH" if match_score>85 else "GOOD MATCH"}
                </div>
            </div>
            """, unsafe_allow_html=True)