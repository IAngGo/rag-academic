"""Concrete PDF parser that extracts text page-by-page using the PyMuPDF (fitz) library."""

from pathlib import Path

import fitz  # PyMuPDF

from rag.domain.ports import PDFParserPort


class PyMuPDFParser(PDFParserPort):
    """Extracts text from a PDF file, returning one (page_number, text) pair per page."""

    def parse(self, file_path: str) -> list[tuple[int, str]]:
        """Open the PDF and return (1-indexed page number, page text) for every page."""
        if not Path(file_path).exists():
            raise FileNotFoundError(f"PDF not found: {file_path}")
        pages: list[tuple[int, str]] = []
        doc = fitz.open(file_path)
        try:
            for page_num, page in enumerate(doc, start=1):
                pages.append((page_num, page.get_text()))
        finally:
            doc.close()
        return pages
