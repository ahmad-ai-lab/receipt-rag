# Project 1: Receipt RAG service

**Goal:** Turn receipt photos and PDFs into validated structured data, then let me search and ask questions with answers that cite their source. Teaches structured outputs, retrieval and reranking.

**Stack:** Python, FastAPI, Postgres with pgvector, Hugging Face reranker. Level: Intermediate, about 17 h.

## Milestones
- [ ] Pydantic schema (merchant, date, line items, total, currency) with a retry that feeds the validation error back to the model
- [ ] Flag receipts where line items do not add up to the total
- [ ] Ingest receipts and PDFs: split by structure, embed, store in pgvector
- [ ] Hybrid search (vector plus keyword) with metadata filters
- [ ] Rerank results with a cross-encoder from the Hugging Face Hub
- [ ] FastAPI endpoints to upload, search and ask, with cited answers
- [ ] pytest tests for extraction and the API

## Edge cases
- Blurry or rotated photo
- Czech and English receipts mixed, dates like 3.10.2026
- Model returns invalid JSON or refuses
- No relevant chunk: answer "I don't know"
- Chunks too small or too large: compare the results
- Same receipt uploaded twice, or updated

## Portfolio proof
Extraction accuracy on 30 labelled receipts, plus hit rate and MRR with and without reranking.

## Project rules
- Retrieval eval: 25 questions, report hit rate and MRR with and without reranking.
- Extraction eval: 30 labelled receipts, failure cases listed in the README.
