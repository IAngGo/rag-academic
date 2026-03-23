# CLAUDE.md — RAG Academic

## Project
- Name: RAG Academic
- Goal: RAG system over academic papers — upload PDFs, ask questions, get answers grounded in document content
- Repo: git@github.com:IAngGo/rag-academic.git
- Owner: Angel — Data Science student transitioning into AI Engineering

## Stack
- PDF parsing: PyMuPDF
- Embeddings: sentence-transformers (all-MiniLM-L6-v2, 384 dimensions)
- Vector store: Supabase pgvector
- API: FastAPI
- Language: Python 3.11+

## Architecture
Hexagonal (strict layers):

- domain/ → entities and abstract ports only. Zero infrastructure imports. Ever.
- application/ → use cases only. Orchestrates domain ports. Zero infrastructure imports. Ever.
- infrastructure/ → concrete implementations (PyMuPDF, sentence-transformers, Supabase, FastAPI)
- Dependency direction: infrastructure → application → domain. Never reversed.

## Development order
1. domain/entities.py
2. domain/ports.py
3. infrastructure/pdf/pymupdf_parser.py
4. infrastructure/embeddings/sentence_transformer_embedder.py
5. infrastructure/vector_store/supabase_store.py
6. application/ingest_document.py
7. infrastructure/api/main.py

## Code standards
- All code, comments, variable names, and documentation in English
- Type hints on every function
- Docstring on every function and module
- Max 200 lines per file — split into modules if needed
- Never hardcode secrets or API keys
- Never skip error handling
- Use .env for all credentials (SUPABASE_URL, SUPABASE_KEY)

## How we work
- Before writing any file: explain what you are about to do and why, break it into steps, wait for OK
- After writing code: explain what each part does
- Never generate code Angel cannot explain
- If something is complex, suggest simpler alternatives first
- Be direct — say when something is wrong or has a better approach

## 20% Rule
At the start of each session, before writing any code:
1. Identify the one core concept this session depends on most
2. Teach the 20% of that concept that explains 80% of what matters
3. Then ask: "What are the most common misconceptions about this?"

One core concept per session. Surfaced naturally as needed. Never overload.

## Session Log Protocol
At the end of every session, generate docs/sessions/session-00X.md with this structure:

### Session 00X — YYYY-MM-DD
**Goal:** what we set out to do this session

**Completed:**
- list of files written or modified

**Decisions made:**
- decision — reason why

**Concepts covered:**
For each concept encountered, document in three dimensions:
- What: internal mechanics
- Why: motivation — why it exists
- Where: practical application in this project

Tag each concept with its area:
[LINEAR ALGEBRA] [ML] [NLP] [INFORMATION RETRIEVAL] [SOFTWARE] [PYTHON]
[DATABASES] [NETWORKING] [API] [DEVOPS] [SECURITY] [LLM] [CLOUD]

Use only the tags relevant to the concept. A concept can have more than one tag.

Example entry:
**[LINEAR ALGEBRA] Vector dot product**
- What: sum of element-wise multiplications of two vectors
- Why: measures directional similarity between vectors without caring about magnitude
- Where: cosine similarity in semantic search — how we rank chunks against a query

**Pending:**
- what was not completed and why

**Next session starts at:** exact file and task
