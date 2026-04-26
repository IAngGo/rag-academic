"""Abstract port interfaces that define the contracts for external adapters."""

from abc import ABC, abstractmethod


class PDFParserPort(ABC):
    """Port for parsing PDF files into raw text."""

    @abstractmethod
    def parse(self, file_path: str) -> list[tuple[int, str]]: ...


class EmbedderPort(ABC):
    """Port for generating vector embeddings from text."""

    @abstractmethod
    def embed(self, text: str) -> list[float]: ...

    @abstractmethod
    def embed_many(self, texts: list[str]) -> list[list[float]]: ...


class VectorStorePort(ABC):
    """Port for storing and retrieving chunks from a vector store."""

    @abstractmethod
    def save_chunks(self, chunks: list) -> None: ...

    @abstractmethod
    def search(self, embedding: list[float], top_k: int) -> list: ...
