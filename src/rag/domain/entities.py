"""Domain layer entities: pure data definitions for documents and their derived chunks.

This module belongs to the domain layer and must not import from application or infrastructure.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Document:
    """A source academic paper loaded from a PDF file."""

    id: str
    filename: str
    raw_text: str


@dataclass
class Chunk:
    """A fixed-size text segment derived from a Document, optionally carrying its embedding vector."""

    id: str
    document_id: str
    text: str
    page_number: int
    embedding: list[float] | None = field(default=None)
