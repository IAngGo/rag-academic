"""Use case: ingest a PDF document by parsing it into chunks, embedding them, and persisting to the vector store."""

from uuid import uuid4

from rag.domain.entities import Chunk
from rag.domain.ports import EmbedderPort, PDFParserPort, VectorStorePort


class IngestDocument:
    """Orchestrates the full ingestion pipeline: parse → chunk → embed → store."""

    def __init__(
        self,
        parser: PDFParserPort,
        embedder: EmbedderPort,
        vector_store: VectorStorePort,
        chunk_size: int = 400,
        chunk_overlap: int = 50,
    ) -> None:
        """Receive all dependencies as ports — no infrastructure imports here."""
        self.parser = parser
        self.embedder = embedder
        self.vector_store = vector_store
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def execute(self, file_path: str) -> str:
        """Ingest a PDF and return the generated document_id."""
        pages = self.parser.parse(file_path)
        document_id = str(uuid4())

        all_chunks: list[Chunk] = []
        for page_number, text in pages:
            all_chunks.extend(self._chunk_page(text, page_number, document_id))

        if not all_chunks:
            raise ValueError(f"No text could be extracted from {file_path}")

        embeddings = self.embedder.embed_many([chunk.text for chunk in all_chunks])
        for chunk, embedding in zip(all_chunks, embeddings):
            chunk.embedding = embedding

        self.vector_store.save_chunks(all_chunks)
        return document_id

    def _chunk_page(self, text: str, page_number: int, document_id: str) -> list[Chunk]:
        """Split a single page's text into overlapping fixed-size chunks."""
        chunks: list[Chunk] = []
        start = 0
        step = self.chunk_size - self.chunk_overlap
        while start < len(text):
            chunk_text = text[start : start + self.chunk_size]
            if chunk_text.strip():
                chunks.append(
                    Chunk(
                        id=f"{document_id}-p{page_number}-{start}",
                        document_id=document_id,
                        text=chunk_text,
                        page_number=page_number,
                    )
                )
            start += step
        return chunks
