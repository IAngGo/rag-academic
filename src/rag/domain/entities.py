"""Domain entities representing the core data structures of the RAG system."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Document:
    id: str
    filename: str
    raw_text: str


@dataclass
class Chunk:
    id: str
    document_id: str
    text: str
    page_number: int
    embedding: Optional[list[float]]
