### Session 001 — 2026-03-22
**Goal:** Project setup, stack decisions, and architecture definition

**Completed:**
- Supabase project created (rag-academic, São Paulo region)
- GitHub repo initialized: git@github.com:IAngGo/rag-academic.git
- Full hexagonal folder structure created and committed to master
- CLAUDE.md created
- .gitignore, .env.example, requirements.txt, README.md created

**Decisions made:**
- Hexagonal architecture over simple layered — system will connect to more services later, avoiding future refactor
- sentence-transformers over OpenAI embeddings — free, local, no API dependency for core pipeline
- Supabase pgvector over Pinecone or ChromaDB — persistent, deployable, shows SQL + vector literacy
- FastAPI from day one — system is designed to be consumed by external services and a future landing page

**Concepts covered:**

**[SOFTWARE] Hexagonal Architecture**
- What: separates business logic from external dependencies via abstract ports and concrete adapters
- Why: makes the system replaceable at the infrastructure level without touching core logic
- Where: changing Supabase for Qdrant only touches infrastructure/vector_store/ — nothing else

**[ML] Embeddings**
- What: dense vector representations of text where semantic similarity = geometric proximity
- Why: allows retrieval by meaning, not keyword matching
- Where: every chunk is embedded and stored; queries are embedded at search time for comparison

**[DATABASES] pgvector**
- What: Postgres extension that adds a vector column type and approximate nearest neighbor search
- Why: keeps vectors inside the relational database alongside metadata, no separate vector DB needed
- Where: Supabase uses it to store chunk embeddings and run similarity queries

**Pending:**
- Enable pgvector extension in Supabase SQL Editor: run `create extension if not exists vector;`
- Write domain/entities.py

**Next session starts at:** domain/entities.py
