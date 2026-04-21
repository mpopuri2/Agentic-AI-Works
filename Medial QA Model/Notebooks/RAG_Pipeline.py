from sentence_transformers import SentenceTransformer, util
from web_data_retrival import fetch_medline
from newspaper import Article
import requests
from bs4 import BeautifulSoup

import re
import unicodedata
from langchain_text_splitters import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import faiss

from transformers import TextIteratorStreamer
from threading import Thread 




def get_page_content(results):
    page_content = []

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    for page in results:
        url = page.get("Link")
        if not url:
            continue

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status() 

            soup = BeautifulSoup(response.text, "html.parser")

            if soup.find("article"):
                main_content = soup.find("article")
            elif soup.find("main"):
                main_content = soup.find("main")
            else:
                main_content = soup 

            text = main_content.get_text(separator="\n").strip()
            title = soup.title.string if soup.title else "No Title"

            page_content.append({"title": title, "content": text})
            print("Fetched text length:", len(text))

        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            continue
    
    return page_content

def clean(text):
    text = unicodedata.normalize("NFKC",text)
    text = re.sub(r"\n+","\n",text)
    text = re.sub(r"\s+"," ",text)
    text = text.strip()
    text = re.sub(r'^\s*[-*•]\s*', '', text, flags=re.MULTILINE)
    return text

def get_top_k_results(model, user_input, chunks,top_k):
    
    model_mini = SentenceTransformer(model)
    q_emb = model_mini.encode([user_input])
    ans_emb = model_mini.encode(chunks)

    top_k_results = util.semantic_search(q_emb,ans_emb,top_k)
    return top_k_results

def retrive_chunks(emb_model,index,user_input, chunks, k = 5):

    if len(chunks) == 0:
        return []

    q_encode = emb_model.encode([user_input], convert_to_numpy=True)

    k = min(k, index.ntotal)
    distance, indices = index.search(q_encode, k)

    return [chunks[i] for i in indices[0] if i < len(chunks)]


def phi_model_load(phi_model,phi_tokenizer,prompt,max_new_tokens = 300):
    inputs = phi_tokenizer(prompt,return_tensors="pt").to(phi_model.device)

    outputs = phi_model.generate(**inputs, max_new_tokens = 300, do_sample = False)

    return phi_tokenizer.decode(outputs[0], skip_special_tokens=True)

def answer_the_question(user_input):
    print(f"The question you entered is : {user_input}")
    results = fetch_medline(user_input,max_results = 7)
    print(results)
    # page_content = get_page_content(results)
    # if len(page_content) == 0:
    #     print("Falling back to snippets")
    #     text = ""
    #     for page in results:
    #         text += page.get("Title") + ":" + page.get("Snippet")
        
    #     print(text)
        
    #     return (
    #         f"I couldn’t retrieve full medical articles from trusted sources for this query. \n Here is a brief summary based on available medical snippets.\n\n {text}"
    #     )
    # text = ""
    # for page in page_content:
    #     text += page.get("title") + ": " + page.get("content") + "\n"
    
    text = clean(results)

    if len(text.strip()) < 200:
        return "⚠️ Unable to retrieve sufficient medical content from trusted sources. Please try a different question."
    
    splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 90,length_function = len)
    chunks = splitter.split_text(text)
    if len(chunks) == 0:
        return "⚠️ No relevant medical context could be extracted for this query."
    
    # top_k_results = get_top_k_results(model = "All-miniLM-L6-V2", user_input=user_input, chunks = chunks, top_k = 15)

    # next_sum = ""
    # for item in top_k_results[0]:
    #     next_sum += chunks[item["corpus_id"]]


    emb_model = SentenceTransformer("All-miniLM-L6-v2")

    ch_encode = emb_model.encode(
        chunks,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    if ch_encode.ndim == 1:
        ch_encode = ch_encode.reshape(1, -1)

    dimensions = ch_encode.shape[1]

    print("Chunks:", len(chunks))
    print("Embedding shape:", ch_encode.shape)

    index = faiss.IndexFlatL2(dimensions)
    index.add(ch_encode)


    context_chunks = retrive_chunks(emb_model,index, user_input,chunks,5)
    context = "\n".join(context_chunks)


    device = "mps" if torch.backends.mps.is_available() else "cpu"

    print("Using Device: ",device)

    phi_model_name = "microsoft/phi-3-mini-4k-instruct"

    phi_tokenizer = AutoTokenizer.from_pretrained(phi_model_name)

    phi_model = AutoModelForCausalLM.from_pretrained(phi_model_name,dtype = torch.float16,device_map = "auto")


    phi_prompt = f"""<|system|>
    You are a medical assistant.
    Answer the following concisely in **TWO paragraphs** using only the context.
    Be concise and factual.
    </|system|>

    <|user|>
    Context:
    {context}

    Question:
    {user_input}

    </|user|>

    <|assistant|>"""

    inputs = phi_tokenizer(phi_prompt,return_tensors="pt").to(phi_model.device)

    streamer = TextIteratorStreamer(phi_tokenizer,skip_prompt=True,skip_special_tokens = True)

    generation_kwargs = dict(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=300,
        temperature=0.2,
        do_sample=False,
        streamer=streamer,
        eos_token_id=phi_tokenizer.eos_token_id,
        pad_token_id=phi_tokenizer.eos_token_id
    )

    thread = Thread(target=phi_model.generate, kwargs=generation_kwargs)
    thread.start()

    generated_text = ""

    for token in streamer:
        yield token

    paragraphs = [p.strip() for p in generated_text.split("\n\n") if p.strip()]

    final_answer = "\n\n".join(paragraphs[:2])
    return final_answer



    