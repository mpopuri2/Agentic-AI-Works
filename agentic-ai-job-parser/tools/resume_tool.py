from openai import OpenAI
from config.settings import OPENAI_API_KEY
from rag.retriever import retrive_relavant_experience

client = OpenAI(api_key = OPENAI_API_KEY)

def tailor_resume(job_description):
    """
    Tailors the master resume to a specific job description.
    Returns structured JSON output.
    """
    #Retrive relevant experience from master resume stores in vector store.
    relevant_context = retrive_relavant_experience(job_description)

    #System Prompt - System constructive prompt to guide the LLM in tailoring the resume.
    system_prompt = """
    You are an expert resume optimization assistant.
    Rewrite resumes to maximize ATS compatibility.
    Focus on:
    - Keywords from job description
    - Quantified achievements
    - Relevant technical skills
    - Clear bullet formatting
    Keep it professional and concise.
    """

    user_prompt = f"""
    JOB DESCRIPTION:
    {job_description}

    RELEVANT EXPERIENCE FROM MASTER RESUME:
    {relevant_context}

    Rewrite the resume section to best match the job.
    Return output in clean bullet-point resume format.
    """

    #call LLM

    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {
                "role": "user", "content" : system_prompt
            },
            {
                "role" : "user", "content" : user_prompt
            }
        ],
        temperature= 0.3
    )
    tailored_resume = response.choices[0].message.content

    return {"tailored_resume" : tailored_resume}
