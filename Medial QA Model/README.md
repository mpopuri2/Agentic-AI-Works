# 🩺 Medical QA Model — AI Health Assistant

An end-to-end **Medical Question Answering** system that combines **Retrieval-Augmented Generation (RAG)** with trusted medical sources (MedlinePlus, PubMed) and a locally-run **Microsoft Phi-3** language model to answer health-related questions accurately and safely.

Ask a medical question — the system retrieves content from authoritative medical databases, embeds and ranks the most relevant passages using semantic search, and generates a concise, grounded answer through a lightweight LLM.

---

## ✨ Features

- **RAG Pipeline** — retrieves context from MedlinePlus & PubMed, chunks it, embeds it, and feeds the top-ranked chunks into the LLM.
- **Trusted Medical Sources** — pulls from MedlinePlus Connect API and PubMed E-utilities (NCBI).
- **Semantic Search with FAISS** — fast vector similarity search over retrieved chunks.
- **Sentence Embeddings** — uses `all-MiniLM-L6-v2` from SentenceTransformers.
- **Local LLM Inference** — runs Microsoft's `phi-3-mini-4k-instruct` locally via Hugging Face Transformers (supports Apple MPS / CUDA / CPU).
- **Streaming Answers** — token-by-token streaming output using `TextIteratorStreamer`.
- **Streamlit Frontend** — simple web interface to ask questions and get answers.

---

## 🧠 How It Works

```
User Question
      │
      ▼
┌──────────────────────────┐
│  MedlinePlus / PubMed    │   ← Retrieve medical content
│     (web_data_retrival)  │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  Clean + Chunk Text      │   ← RecursiveCharacterTextSplitter
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  Embed Chunks            │   ← SentenceTransformer (MiniLM-L6-v2)
│  Store in FAISS Index    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  Retrieve Top-K Chunks   │   ← Semantic search vs. question
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  Phi-3 Mini (4K Instruct)│   ← Generates grounded answer
└────────────┬─────────────┘
             │
             ▼
     Streamed Answer → UI
```

---

## 📁 Project Structure

```
Medical QA Model/
├── Datasets/
│   └── medquad.csv                 # MedQuAD medical Q&A dataset
├── Notebooks/
│   ├── RAG_Pipeline.py             # Core RAG pipeline (retrieval + embedding + generation)
│   ├── web_data_retrival.py        # MedlinePlus & PubMed fetchers
│   ├── app.py                      # Streamlit web interface
│   ├── API_TEST.py                 # API sanity tests
│   ├── scipy_test.py               # Environment/dependency checks
│   ├── Basic_search_model.ipynb    # Baseline semantic search experiments
│   ├── base_model_dataset.ipynb    # Dataset exploration & baseline
│   ├── collab_run_file.ipynb       # Colab-ready runner
│   └── medline.ipynb               # MedlinePlus API experiments
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/Medical-QA-Model.git
cd "Medical QA Model"
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate         # macOS/Linux
venv\Scripts\activate            # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not present, install manually:

```bash
pip install streamlit sentence-transformers transformers torch faiss-cpu \
            langchain-text-splitters newspaper3k beautifulsoup4 requests
```

---

## 🚀 Running the App

From the `Notebooks/` directory:

```bash
cd Notebooks
streamlit run app.py
```

Then open the URL shown in your terminal (typically http://localhost:8501).

Type a medical question (e.g., *"What is a heart attack?"*) and hit **ASK**.

---

## 🧩 Core Components

### `RAG_Pipeline.py`
The brains of the system. Handles:
- `fetch_medline(query)` — retrieves data from MedlinePlus
- `clean(text)` — normalizes unicode, whitespace, and list markers
- `RecursiveCharacterTextSplitter` — chunks text (size=500, overlap=90)
- Embedding with `all-MiniLM-L6-v2`
- FAISS `IndexFlatL2` for similarity search
- `phi-3-mini-4k-instruct` for final answer generation
- Streaming output via `TextIteratorStreamer`

### `web_data_retrival.py`
Handles data retrieval from:
- **MedlinePlus Connect API** (`https://connect.medlineplus.gov/service`)
- **PubMed E-utilities** (`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/`)
- Includes fallback logic: if MedlinePlus content is too short, it queries PubMed.

### `app.py`
Streamlit UI with:
- Question input box
- Streaming answer display
- Medical disclaimer banner

---

## 📊 Dataset

**MedQuAD** (Medical Question Answering Dataset) — located in `Datasets/medquad.csv`.
Contains ~47K question-answer pairs curated from trusted NIH medical resources, used for baseline evaluation and experimentation.

---

## 🖥️ Hardware Support

The pipeline automatically selects the best available device:

| Platform   | Device |
|------------|--------|
| Apple Silicon (M1/M2/M3) | `mps` |
| NVIDIA GPU | `cuda` |
| Fallback   | `cpu`  |

Phi-3 Mini (~3.8B params) runs comfortably on 16GB+ RAM machines with GPU/MPS acceleration.

---

## ⚠️ Disclaimer

This project is for **educational and research purposes only**. The answers generated by this system are **not medical advice** and should not be used as a substitute for consultation with a qualified healthcare professional. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

---

## 🛠️ Tech Stack

- **Python 3.13**
- **Streamlit** — web UI
- **Hugging Face Transformers** — LLM (Phi-3 Mini)
- **SentenceTransformers** — embeddings
- **FAISS** — vector similarity search
- **LangChain Text Splitters** — chunking
- **Requests / BeautifulSoup** — web + API scraping
- **PyTorch** — model inference backend

---

## 🔮 Roadmap

- [ ] Add requirements.txt and Dockerfile
- [ ] Add unit tests for retrieval + embedding layers
- [ ] Persist FAISS index to disk to avoid recomputing
- [ ] Add support for larger models (Phi-3-medium, Llama-3) via config
- [ ] Evaluation harness over MedQuAD with BLEU / ROUGE / factuality metrics
- [ ] Deploy as a hosted Streamlit Cloud / Hugging Face Space demo

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes
4. Push to the branch
5. Open a PR

---

## 📜 License

This project is released under the **MIT License**. See `LICENSE` file for details.

---

## 👤 Author

**Manjunath Popuri**
📧 popurimanjunath2001@gmail.com

If you found this project helpful, consider giving it a ⭐ on GitHub!
