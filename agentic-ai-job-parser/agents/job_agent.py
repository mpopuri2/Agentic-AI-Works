from typing import TypedDict, Optional

from langgraph.graph import StateGraph, END

from tools.resume_tool import tailor_resume
from tools.cover_letter_tool import generate_cover_letter
from databse.job_tracker import application_exists, save_application

class JobAgentState(TypedDict):
    company : str
    role : str
    link : str
    job_description : str
    resume : Optional[str]
    cover_letter : Optional[str]
    status : Optional[str]


def resume_node(state: JobAgentState):
    print("Running Resume Agent...")
    tailored_resume = tailor_resume(state["job_description"])

    state["resume"] = tailored_resume["tailored_resume"]

    return state

def cover_letter_node(state: JobAgentState):
    print("Running Cover Letter Agent...")
    cover_letter = generate_cover_letter(state["job_description"], state["resume"])

    state["cover_letter"] = cover_letter["cover_letter"]

    return state

def application_node(state: JobAgentState):
    print("Application is saving to PostgreSQL...!")

    save_application(company=state["company"],role = state["role"], link = state["link"],resume = state["resume"],cover_letter = state["cover_letter"])

    state["status"] = "saved"
    return state
    

def build_job_agent():
    graph = StateGraph(JobAgentState)

    #adding nodes to graph
    graph.add_node("resume",resume_node)
    graph.add_node("cover_letter",cover_letter_node)
    graph.add_node("save",application_node)

    #the Flow
    graph.set_entry_point("resume")
    graph.add_edge("resume","cover_letter")
    graph.add_edge("cover_letter","save")
    graph.add_edge("save",END)

    return graph.compile()

    




