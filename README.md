# Knowledge-Base Search Engine (RAG demo)

## Overview
A simple Retrieval-Augmented Generation (RAG) demo:
- Ingest PDF/TXT → chunk → embed (sentence-transformers)
- Index with FAISS
- Query via FastAPI → retrieve top-K chunks → synthesize an answer with a small HF LLM (flan-t5-base)
- Optional: swap HF LLM for Google Gemini (see note)

## Run locally (recommended)
1. Create and activate venv
2. `pip install -r backend/requirements.txt`
3. `cd backend`
4. `uvicorn main:app --reload --port 8000`
5. `POST /upload` to add docs
6. `POST /query` to query

## Run on Colab
Paste code into Colab cells, install requirements, and run ingestion & queries inline. For large models, choose GPU runtime.

## Gemini optional
You may use Google Gemini instead of the local LLM for synthesis (requires API key). Gemini has a free tier with limits; check Google Gemini docs.

## Deliverables
- Source code (this repo)
- Demo video: record a short screencast showing ingestion + query results
