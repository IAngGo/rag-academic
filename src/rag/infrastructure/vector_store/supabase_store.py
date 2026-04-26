"""Concrete vector store that persists and queries chunk embeddings via Supabase pgvector."""

import os

from supabase import Client, create_client

from rag.domain.entities import Chunk
from rag.domain.ports import VectorStorePort


class SupabaseVectorStore(VectorStorePort):
    """Persists and retrieves Chunk embeddings using Supabase pgvector."""

    def __init__(self) -> None:
        """Create the Supabase client from environment variables."""
        self.client: Client = create_client(
            os.environ["SUPABASE_URL"],
            os.environ["SUPABASE_KEY"],
        )

    def save_chunks(self, chunks: list[Chunk]) -> None:
        """Upsert all chunks into the chunks table, including their embedding vectors."""
        rows = [
            {
                "id": chunk.id,
                "document_id": chunk.document_id,
                "text": chunk.text,
                "page_number": chunk.page_number,
                "embedding": chunk.embedding,
            }
            for chunk in chunks
        ]
        self.client.table("chunks").upsert(rows).execute()

    def search(self, embedding: list[float], top_k: int) -> list[Chunk]:
        """Return the top_k chunks most similar to the given embedding vector."""
        result = self.client.rpc(
            "match_chunks",
            {"query_embedding": embedding, "match_count": top_k},
        ).execute()
        return [
            Chunk(
                id=row["id"],
                document_id=row["document_id"],
                text=row["text"],
                page_number=row["page_number"],
                embedding=None,
            )
            for row in result.data
        ]
