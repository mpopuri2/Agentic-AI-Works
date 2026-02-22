from openai import OpenAI
from config.settings import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)

def generate_cover_letter(job_description, tailored_resume):

    """
    Generates a personalized cover letter based on job description
    and tailored resume content.
    """

    system_prompt = """
    You are an expert career assistant.
    Write professional, concise, and personalized cover letters.

    Guidelines:
    - Address the role and company (if mentioned)
    - Highlight relevant skills and achievements
    - Keep tone confident and professional
    - Length: 250–300 words
    - Avoid generic phrases
    """

    user_prompt = f"""
    JOB DESCRIPTION:
    {job_description}

    CANDIDATE PROFILE (Tailored Resume Content):
    {tailored_resume}

    Write a personalized cover letter for this role.
    """

    response = client.chat.completions.create(
        model = "gpt-4o-mini",

        messages = [
            { "role" : "user","content" : system_prompt },{ "role":"user","content" : user_prompt }
        ],
        temperature= 0.4
    )

    cover_letter = response.choices[0].message.content

    return { "cover_letter" : cover_letter }

