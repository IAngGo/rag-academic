"""FastAPI application entry point: wires up dependencies and registers route handlers."""

import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

from rag.application.ingest_document import IngestDocument
from rag.application.query_documents import QueryDocuments
from rag.infrastructure.api.models import ChunkResult, IngestResponse, QueryRequest
from rag.infrastructure.embeddings.sentence_transformer_embedder import SentenceTransformerEmbedder
from rag.infrastructure.pdf.pymupdf_parser import PyMuPDFParser
from rag.infrastructure.vector_store.supabase_store import SupabaseVectorStore

app = FastAPI(title="RAG Academic")

_parser = PyMuPDFParser()
_embedder = SentenceTransformerEmbedder()
_vector_store = SupabaseVectorStore()
_ingest_use_case = IngestDocument(_parser, _embedder, _vector_store)
_query_use_case = QueryDocuments(_embedder, _vector_store)


@app.post("/ingest", response_model=IngestResponse)
async def ingest(file: UploadFile = File(...)) -> IngestResponse:
    """Upload a PDF and ingest it into the vector store."""
    if not file.filename or not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    content = await file.read()
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        document_id = _ingest_use_case.execute(tmp_path)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    return IngestResponse(document_id=document_id)


@app.post("/query", response_model=list[ChunkResult])
def query(request: QueryRequest) -> list[ChunkResult]:
    """Embed a query and return the most relevant chunks."""
    try:
        chunks = _query_use_case.execute(request.query, request.top_k)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return [
        ChunkResult(
            id=chunk.id,
            document_id=chunk.document_id,
            text=chunk.text,
            page_number=chunk.page_number,
        )
        for chunk in chunks
    ]
