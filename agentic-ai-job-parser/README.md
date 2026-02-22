
# 🤖 AI Job Platform – Agentic AI Job Search & Application System

An end-to-end **Agentic AI Job Platform** that helps you discover jobs, analyze fit, generate tailored applications, and track submissions.

This project demonstrates a **production-style AI system** built with LangGraph, Streamlit, PostgreSQL, and real-time job APIs.

---

## 🚀 Features

### 🔎 Job Search
- Fetch real-time jobs using **JSearch (RapidAPI)**
- Search by role and location
- Control number of jobs fetched
- Clean card-based UI showing:
  - Job Title
  - Company
  - Location
  - Job Type
  - Date Posted

---

### 🎯 Match Score
- Each job displays an AI-style **Match Score (75–98%)**
- Helps prioritize high-fit roles

---

### 📄 Application Tools
Each job card includes:
- **Apply** – Opens job link in new tab
- **Tailor Resume** - Generates job-specific resume
- **Cover Letter** - Generates customized cover letter

---

### 🧠 LangGraph Agent Flow

Resume → Cover Letter → Save to PostgreSQL

Automates the application workflow using agent orchestration.

---

### 🗄 PostgreSQL Tracking
Stores:
- Company
- Role
- Job Link
- Date Applied
- Resume
- Cover Letter
- Status

Prevents duplicate applications.

---

### 📊 Streamlit Dashboard
- Modern SaaS-style layout
- Dynamic job cards
- Multi-page navigation
- Detailed job view page

---

## 🏗 Project Structure

```
agentic-ai-job-platform/
│
├── app.py
├── web_page_app.py
│
├── utils/
│   └── job_search_tool.py
│
├── tools/
│   ├── resume_tool.py
│   └── cover_letter_tool.py
│
├── database/
│   └── postgres_tracker.py
│
├── agents/
│   └── job_agent.py
│
├── pages/
│   ├── job_search.py
│   └── job_details.py
│
└── requirements.txt
```

---

## ⚙️ Tech Stack

**Frontend**
- Streamlit
- Custom CSS

**Backend / AI**
- Python
- LangGraph
- OpenAI / LLM APIs

**Database**
- PostgreSQL
- psycopg2

**APIs**
- JSearch (RapidAPI)

---

## 🔑 Setup

### 1. Clone Repository
```
git clone https://github.com/yourusername/ai-job-platform.git
cd ai-job-platform
```

### 2. Create Virtual Environment
```
python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

---

### 4. Add API Keys

**RapidAPI (JSearch)**

In `utils/job_search_tool.py`:
```
RAPIDAPI_KEY = "YOUR_KEY"
```

**OpenAI**
```
export OPENAI_API_KEY=your_key
```

---

### 5. Setup PostgreSQL

Create database:
```
createdb job_tracker
```

Update DB config:
```
postgresql://username:password@localhost:5432/job_tracker
```

Initialize table by running your database module.

---

### 6. Run App
```
streamlit run web_page_app.py
```

Open:
```
http://localhost:8501
```

---

## Application Screenshots

### Basic Webpage
<p align="center">
  <img src="results/start_page.heic" width="800">
</p>

### Jobs Dashboard
<p align="center">
  <img src="results/overview_page.heic" width="800">
</p>

### Job Details Page
<p align="center">
  <img src="results/job_description.heic" width="800">
</p>

## 📸 UI Highlights
- Clean job cards
- Right-side action buttons
- Match score panel
- Multi-page navigation
- Real-time job fetching

---

## 🎯 Use Cases
- AI-powered job assistant
- Automated application workflow
- Resume personalization
- Portfolio project for:
  - Data Scientist
  - ML Engineer
  - AI Engineer
  - GenAI Engineer

---

## 📈 Future Enhancements
- Real match scoring using embeddings
- RAG-based resume optimization
- Job description summarization
- Application analytics dashboard
- Email automation
- LinkedIn integration

---

## 👤 Author

**Manjunath Popuri**  
Applied Data Scientist | LLMs | Agentic AI Systems

---

## ⭐ If you like this project
Star the repo and feel free to contribute!
