# 💬 Ask About Me

> An AI-powered personal knowledge assistant that uses Retrieval-Augmented Generation (RAG) to answer questions about my skills, experience, projects, certifications, and technical background.

---

## 📌 Overview

**Ask About Me** is a personal AI assistant designed to make my professional profile interactive.

Instead of requiring someone to read through multiple resumes, project descriptions, and certification documents, users can simply ask questions in natural language.

For example:

- What programming languages does Disha know?
- Tell me about her AI projects.
- What certifications does she have?
- What technologies has she worked with?
- Does she have experience with Python?

The system retrieves relevant information from a collection of personal documents and passes that information to a Large Language Model (LLM), which generates a concise, context-grounded response.

The project uses a **Retrieval-Augmented Generation (RAG)** architecture to reduce hallucinations and ensure that responses are based on the information available in the knowledge base.

---

## 🎯 Problem Statement

Traditional resumes and portfolios are static documents.

A recruiter or interviewer may need to:

1. Open the resume.
2. Search through different sections.
3. Look through project descriptions.
4. Check certifications separately.
5. Determine whether a particular skill or technology is present.

This becomes inconvenient when information is distributed across multiple documents.

**Ask About Me** solves this problem by converting personal documents into an interactive, searchable AI knowledge base.

Instead of manually searching through documents, users can ask a natural-language question and receive a relevant answer.

### Traditional Approach

```text
Resume → Search → Find information → Read → Interpret

User Question
      ↓
Semantic Search
      ↓
Relevant Information
      ↓
LLM
      ↓
Personalized Answer

Personal Documents
       ↓
Document Loading
       ↓
Text Splitting
       ↓
Embedding Generation
       ↓
FAISS Vector Database
       ↓
Semantic Retrieval
       ↓
Relevant Context
       ↓
RAG Prompt
       ↓
Llama 3.1
       ↓
Generated Answer


---

## ▶️ Quick start

```bash
pip install -r requirements.txt
cp .env.example .env        # add your free GROQ_API_KEY
python -m src.ingest        # build the index (re-run whenever files in data/ change)
streamlit run app.py        # UI (runs the RAG chain directly)
# optional REST API: uvicorn api:app --reload   -> POST /ask {"question": "...", "history": []}
```

Edit `data/profile/profile.md` to keep the core facts (contact, education, summary) accurate.
