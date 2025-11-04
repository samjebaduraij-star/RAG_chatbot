# test_documents.py
# Description: Pytest for document handling
# Author: AI Generated Code
# Created: August 15, 2025

import pytest
from backend.app.services.document_service import DocumentService
from backend.app.models.document_models import Document

def test_add_and_get_document():
    service = DocumentService()
    doc = Document(
        id="doc001",
        filename="test.pdf",
        file_type="application/pdf",
        processed_at="2025-08-15T19:31:00",
        metadata={},
        chunks=[],
        chunk_count=0,
        total_characters=0,
        total_words=0
    )
    service.add_document(doc)
    retrieved = service.get_document("doc001")
    assert retrieved.filename == "test.pdf"