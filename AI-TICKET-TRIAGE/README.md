# LLM-Powered Ticket Triage System

An AI system that automatically classifies customer support tickets, detects urgency, generates response drafts, and routes them to the correct team.

## What It Does

- Classifies tickets into 7 categories (billing, refund, technical, fraud, feature request, account, general)
- Detects urgency (low, normal, high, critical) with keyword-based safety overrides
- Generates empathetic response drafts grounded in company policy using RAG
- Routes tickets to the responsible team automatically
- Learns from human agent corrections over time

## Tech Stack

Python, FastAPI, OpenAI GPT-4o-mini, FAISS, SQLAlchemy, Streamlit, scikit-learn

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add your OpenAI key to `.env`:

```
OPENAI_API_KEY=sk-your-key-here
```

Run the server:

```bash
uvicorn app.main:app --reload --port 8000
```

Test at: http://127.0.0.1:8000/docs
