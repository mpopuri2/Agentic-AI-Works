import streamlit as st
from RAG_Pipeline import answer_the_question

# import streamlit as st
# st.set_option("server.fileWatcherType", "none")

st.set_page_config(page_title="Medical QA Assistant")
st.title("🩺  Medico Answer Assistant")
st.write("Ask a medical question and get an answer from trusted sources.")
user_input = st.text_input("Ask a Question?", placeholder="e.g., What is a heart attack?")

ask_button = st.button("ASK")

if ask_button:
    if not user_input:
        st.warning("Please Enter the Question!")
    else:
        st.header(f"Question : {user_input}")
        st.subheader("Answer :")

        placeholder = st.empty()
        generated_text = ""

        with st.spinner("Generating Answer..."):
            for token in answer_the_question(user_input):
                generated_text += token
                placeholder.markdown(generated_text)

        st.info("⚠️ This information is for educational purposes only and not medical advice.")