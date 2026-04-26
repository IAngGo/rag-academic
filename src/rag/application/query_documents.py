"""Use case: accept a natural-language query, embed it, and retrieve the most relevant chunks from the vector store."""

from rag.domain.entities import Chunk
from rag.domain.ports import EmbedderPort, VectorStorePort


class QueryDocuments:
    """Embeds a query and retrieves the top-k most similar chunks from the vector store."""

    def __init__(self, embedder: EmbedderPort, vector_store: VectorStorePort) -> None:
        """Receive dependencies as ports — no infrastructure imports here."""
        self.embedder = embedder
        self.vector_store = vector_store

    def execute(self, query: str, top_k: int = 5) -> list[Chunk]:
        """Embed the query and return the top_k most relevant chunks."""
        if not query.strip():
            raise ValueError("Query cannot be empty.")
        embedding = self.embedder.embed(query)
        return self.vector_store.search(embedding, top_k)
