### Session 002 — 2026-04-26
**Goal:** Implement the full RAG pipeline — parser, embedder, vector store, use cases, and API

**Completed:**
- `domain/ports.py` — updated `PDFParserPort.parse` signature to `list[tuple[int, str]]` to preserve page numbers
- `infrastructure/pdf/pymupdf_parser.py` — PyMuPDF parser with per-page text extraction
- `infrastructure/embeddings/sentence_transformer_embedder.py` — sentence-transformers embedder with batch support
- `infrastructure/vector_store/supabase_store.py` — Supabase pgvector store with upsert and RPC search
- `application/ingest_document.py` — IngestDocument use case with sliding window chunking
- `application/query_documents.py` — QueryDocuments use case
- `infrastructure/api/main.py` + `models.py` — FastAPI endpoints for /ingest and /query
- Supabase: pgvector extension enabled, `chunks` table created, `match_chunks` SQL function created

**Decisions made:**
- `PDFParserPort.parse` returns `list[tuple[int, str]]` instead of `str` — preserves page-number information needed by `Chunk.page_number`; losing it would make the field meaningless
- Chunking lives in the use case, not the parser — parser extracts raw text, use case decides how to split it
- Chunk size 400 chars / 50 overlap — ~80-100 tokens, well within all-MiniLM-L6-v2's 256-token limit; overlap prevents ideas from being split at boundaries
- RLS disabled on `chunks` table — frontend will call FastAPI, not Supabase directly; Supabase key never leaves the server
- Infrastructure instances wired at module level in `main.py` — embedding model loads once on startup, not per request
- Temp file for PDF uploads — PyMuPDF requires a path on disk, not a bytes object; deleted in `finally` to avoid leaks

**Concepts covered:**

**[NLP] [INFORMATION RETRIEVAL] Text Chunking with Sliding Window**
- What: splits a long text into fixed-size overlapping segments by advancing a window of size N by step (N - overlap) each iteration
- Why: embedding models have a token limit (~256 for all-MiniLM-L6-v2); chunking at fixed intervals without overlap risks splitting a single idea across two chunks, losing context at the boundary
- Where: `IngestDocument._chunk_page` — 400-char window, 50-char overlap, applied per page

**[SOFTWARE] Dependency Injection via Constructor**
- What: a class receives its dependencies as constructor parameters instead of instantiating them internally
- Why: the use case layer must not import from infrastructure; injecting ports as abstractions keeps the dependency direction correct (infrastructure → application → domain, never reversed)
- Where: `IngestDocument.__init__` and `QueryDocuments.__init__` receive ports, never concrete classes

**[DATABASES] pgvector RPC Pattern**
- What: the `<=>` cosine distance operator in pgvector is not exposed by Supabase's REST API; to use it you must wrap the query in a SQL function and call it via `.rpc()`
- Why: Supabase's auto-generated REST API only covers basic CRUD; custom operators require a server-side function
- Where: `match_chunks` SQL function in Supabase, called from `SupabaseVectorStore.search`

**[API] Temporary File Pattern for File Uploads**
- What: write uploaded bytes to a `NamedTemporaryFile`, pass the path to the processing function, delete the file in a `finally` block
- Why: some libraries (PyMuPDF) require a file path on disk rather than an in-memory bytes object; `finally` guarantees cleanup even if processing raises an exception
- Where: `POST /ingest` in `main.py`

**[ML] Batch Embedding**
- What: passing a list of texts to `model.encode()` in one call instead of calling it once per text
- Why: the model processes the full batch in a single forward pass through the neural network, which is significantly faster than N individual passes due to parallelism and amortized overhead
- Where: `SentenceTransformerEmbedder.embed_many`, called in `IngestDocument.execute` after all chunks are collected

**Pending:**
- Test the full pipeline: start the server, upload a real PDF, run a query, verify results
- Add `.env` file with `SUPABASE_URL` and `SUPABASE_KEY` (not committed — in `.gitignore`)

**Next session starts at:** testing the pipeline end-to-end with a real PDF
