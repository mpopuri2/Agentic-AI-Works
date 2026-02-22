# from openai import OpenAI
# from config.settings import OPENAI_API_KEY

# client = OpenAI(api_key = OPENAI_API_KEY)

# def test_llm():
#     response = client.chat.completions.create(
#         model = "gpt-4o-mini",
#         messages = [
#             {
#                 "role" : "user",
#                 "content" : "Say hello from our Agentic AI system."
#             }
#         ]
#     )

#     print(response.choices[0].message.content)

# if  __name__ == "__main__":
#     test_llm()

# from rag.retriever import retrive_relavant_experience
# if __name__ == "__main__":
#     job_descrription = "We are looking for a Machine Learning Engineer with experience in Python, AWS, model deployment, and building scalable ML pipelines."

#     context = retrive_relavant_experience(job_descrription)
#     print("Retrived Resume Contect : \n")
#     print(context)

# from tools.resume_tool import tailor_resume
# from tools.cover_letter_tool import tailor_cover_letter

# if __name__ == "__main__":
#     job_description = """
#     We are hiring a Machine Learning Engineer with strong experience in
#     Python, AWS, scalable ML pipelines, model deployment,
#     and production AI systems.
#     """

#     result = tailor_resume(job_description)

#     print("\n=== Tailored Resume ===\n")
#     print(result["tailored_resume"])

#     cover_letter = generate_cover_letter(job_description, result["tailored_resume"])

#     print("\n=== Tailored Cover Letter ===\n")
#     print(cover_letter["cover_letter"])

# from databse.job_tracker import initialize_db, save_application, get_all_Applications

# if __name__ == "__main__":
#     initialize_db()
#     save_application(company = "ABC",role = "abc Engineer",link = "https://wwww.abc.com/x/12346", status = "Applied", resume = "ABC", cover_letter = "ABC")
#     applications = get_all_Applications()

#     print("\n === All Job Applications ===\n")

#     for app in applications:
#         print(app)

from agents.job_agent import build_job_agent
from databse.job_tracker import initialize_db


if __name__ == "__main__":
    initialize_db()
    agent = build_job_agent()
    initial_state= {
        "company" : "Apple",
        "role" : "AI Engineer",
        "link" : "https://www.apple.com/",
        "job_description" : """We are looking for a Machine Learning Engineer with experience in Python, AWS, model deployment, and scalable ML systems.""",
        "resume" : None,
        "cover_letter" : None,
        "status":None
    }

    result = agent.invoke(initial_state)

    print("\nFinal State : \n")
    # print(result)

    print("\n"+"-"*25)
    print(result["company"])

    print("\n"+"-"*25)

    print(result["role"])
    print("\n"+"-"*25)
    print(result["link"])
    print("\n"+"-"*25)
    print(result["status"])
    print("\n"+"-"*25)

    print("\n"+"-"*25)
    print(result["resume"])

    print("\n"+"-"*25)

    print(result["cover_letter"])

    print("\n"+"-"*25)
