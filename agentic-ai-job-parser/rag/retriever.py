from rag.vector_store import load_vector_store

def retrive_relavant_experience(job_description,k=4):
    vectorstore = load_vector_store()
    docs = vectorstore.similarity_search(job_description, k=k)
    return "\n\n".join([doc.page_content for doc in docs])
