---
title: AI Study Bot
emoji: 📚
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: "1.0"
app_port: 7860
pinned: false
---

# 📚 Study Bot — PDF-Based RAG Study Assistant

A retrieval-augmented generation (RAG) system that lets you upload a PDF and ask questions about it — answers are grounded in your document's content, not hallucinated by the model.

Built with FastAPI, ChromaDB, Sentence-Transformers, and Groq's Llama 3.1.

---

## 🎯 What It Does

- Upload any PDF (lecture notes, textbooks, research papers)
- Ask natural language questions about the content
- Get answers grounded strictly in the document — if the answer isn't in the PDF, it says so
- View which chunks of text were retrieved to generate each answer (RAG transparency)

---

## 🏗️ Architecture
┌─────────────────┐         ┌──────────────────────────────────────┐
│                 │  HTTP   │           FastAPI Backend             │
│  Streamlit      │ ──────► │                                      │
│  Frontend       │         │  1. PDF Upload → PyPDF chunking      │
│                 │ ◄────── │  2. Sentence-Transformers embeddings │
│  front.py       │         │  3. ChromaDB vector storage          │
└─────────────────┘         │  4. Semantic search on query         │
│  5. Groq Llama 3.1 answer generation │
└──────────────────────────────────────┘

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| Embeddings | Sentence-Transformers (`all-MiniLM-L6-v2`) |
| Vector Database | ChromaDB |
| LLM | Groq API (Llama 3.1) |
| PDF Parsing | PyPDF |
| Language | Python 3.13 |

---

## ✅ Evaluation

Tested against 13 retrieval scenarios using a custom evaluation harness:
- **92%+ keyword-match accuracy** across all test cases
- Hallucination guard confirmed — questions outside document scope return "I don't know based on the provided context" rather than fabricated answers

---

## 🚀 Running Locally

### Prerequisites
- Python 3.11+
- A Groq API key (free at [console.groq.com](https://console.groq.com))

### Setup

**1. Clone the repo**
```bash
git clone https://github.com/7rysh/AI-Study-Bot.git
cd AI-Study-Bot
```

**2. Create and activate a virtual environment**
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Mac/Linux
python -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r backend/requirements.txt
```

**4. Set up your API key**

Create a file at `backend/.env`:
GROQ_API_KEY=your_key_here

**5. Start the backend**
```bash
cd backend
uvicorn main:app --reload
```

**6. Start the frontend** (new terminal)
```bash
cd frontend
streamlit run front.py
```

**7. Open your browser at** `http://localhost:8501`

---

## 📁 Project Structure
AI-Study-Bot/
├── backend/
│   ├── main.py                 # FastAPI app and endpoints
│   ├── requirements.txt        # Python dependencies
│   ├── eval_harness.py         # Evaluation test suite
│   ├── services/
│   │   ├── embedding_service.py   # Sentence-Transformers integration
│   │   ├── pdf_service.py         # PDF parsing and chunking
│   │   └── rag_service.py         # RAG pipeline and Groq integration
│   └── .env                    # API keys (not tracked)
└── frontend/
└── front.py                # Streamlit UI

---

## 🔑 Key Implementation Details

- **Semantic chunking** — PDFs are split with overlap to preserve context across chunk boundaries
- **Context-constrained prompting** — the LLM is explicitly instructed to answer only from retrieved context, reducing hallucination
- **RAG transparency** — the frontend displays which source chunks were used to generate each answer
- **Evaluation harness** — `eval_harness.py` runs 13 test questions against the live API and reports keyword-match accuracy

---

## 🔮 Planned Improvements

- Fix chunking boundary issue affecting short sections (Summary, project lists)
- Duplicate chunk handling on re-upload
- Public deployment on Hugging Face Spaces
- Docker containerization
