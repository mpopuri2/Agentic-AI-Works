import streamlit as st

st.set_page_config(page_title="Job Details", layout="wide")

job = st.session_state.get("selected_job")

if not job:
    st.warning("No job selected")
    st.stop()

st.title("Job Details")

# Back button
if st.button("⬅ Back to Dashboard"):
    st.session_state.page = "home"
    st.switch_page("web_page_app.py")

st.markdown("---")

# Job Header Card
st.markdown(
    f"""
    <div style="
        background:linear-gradient(135deg,#2563eb,#4f46e5);
        color:white;
        padding:25px;
        border-radius:15px;
        margin-bottom:20px;
    ">
        <h2>{job['title']}</h2>
        <h4>{job['company']}</h4>
        <p>
        📍 {job['job_location']} | 
        🕒 {job['date_posted']} | 
        💼 {job['job_type']}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Description Section
st.subheader("Job Description")

st.markdown(
    f"""
    <div style="
        background-color:#f9fafb;
        padding:20px;
        border-radius:10px;
        line-height:1.6;
        color:#374151;
    ">
    {job['description'] if job['description'] else "No description available"}
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# Action Buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Apply Now"):
        st.markdown(f"[Open Application]({job['link']})")

with col2:
    if st.button("Tailor Resume"):
        st.success("Resume tailoring started")

with col3:
    if st.button("Generate Cover Letter"):
        st.success("Cover letter generating")