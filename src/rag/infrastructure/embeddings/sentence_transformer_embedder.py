"""Concrete embedder that generates dense vector representations using a Sentence Transformers model."""

from sentence_transformers import SentenceTransformer

from rag.domain.ports import EmbedderPort


class SentenceTransformerEmbedder(EmbedderPort):
    """Wraps a Sentence Transformers model to produce fixed-size embedding vectors."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        """Load the model once at construction time."""
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list[float]:
        """Return the embedding vector for a single text string."""
        return self.model.encode([text])[0].tolist()

    def embed_many(self, texts: list[str]) -> list[list[float]]:
        """Return embedding vectors for a batch of texts in one forward pass."""
        return [vec.tolist() for vec in self.model.encode(texts)]
