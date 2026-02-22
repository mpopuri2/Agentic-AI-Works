import os
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from config.settings import OPENAI_API_KEY

DATA_PATH = "data/resume.txt"
VECTOR_PATH = "rag/faiss_index"

def load_resume():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Resume file not found at {DATA_PATH}")
    
    with open(DATA_PATH,"r",encoding="utf-8") as f:
        return f.read()

def create_vector_store():
    text = load_resume()

    #chunk the resume.
    spllitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 100
    )
    chunks = spllitter.split_text(text)
    
    # Embeddiings
    embeddings = OpenAIEmbeddings(
        model = "text-embedding-3-small",
        api_key = OPENAI_API_KEY
    )

    #create FAISS index
    vector_store = FAISS.from_texts(chunks,embeddings)

    #Save Locally
    vector_store.save_local(VECTOR_PATH)

    print(f"Vector store created with {len(chunks)} chunks.")

def load_vector_store():
    embeddings = OpenAIEmbeddings(
        model = "text-embedding-3-small",
        api_key = OPENAI_API_KEY
    )
    return FAISS.load_local(VECTOR_PATH, embeddings, allow_dangerous_deserialization=True)
