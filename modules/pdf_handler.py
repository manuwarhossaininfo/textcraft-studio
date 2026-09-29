"""
PDF Handler - Extract text from PDF files
"""

import io
from typing import Optional

try:
    from PyPDF2 import PdfReader
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


class PDFHandler:
    """Handles PDF file processing and text extraction."""

    @staticmethod
    def is_available() -> bool:
        return PDF_AVAILABLE

    @staticmethod
    def extract_text(file_bytes: bytes) -> Optional[str]:
        """Extract text from PDF bytes."""
        if not PDF_AVAILABLE:
            return None

        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            text_parts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            full_text = "\n\n".join(text_parts)
            return full_text.strip() if full_text.strip() else None
        except Exception as e:
            return None

    @staticmethod
    def get_page_count(file_bytes: bytes) -> int:
        """Get number of pages in PDF."""
        if not PDF_AVAILABLE:
            return 0
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            return len(reader.pages)
        except Exception:
            return 0