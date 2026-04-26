"""Pydantic schemas for HTTP request and response bodies used by the FastAPI routes."""

from pydantic import BaseModel, Field


class IngestResponse(BaseModel):
    """Returned after a PDF is successfully ingested."""

    document_id: str


class QueryRequest(BaseModel):
    """Body for the /query endpoint."""

    query: str
    top_k: int = Field(default=5, ge=1, le=20)


class ChunkResult(BaseModel):
    """A single retrieved chunk returned by the /query endpoint."""

    id: str
    document_id: str
    text: str
    page_number: int
