# document_service.py
# Description: Business logic for document upload and processing
# Dependencies: backend/app/models/document_models.py
# Author: AI Generated Code
# Created: August 15, 2025

from backend.app.models.document_models import Document
from typing import Dict

class DocumentService:
    """Handles document storage and retrieval."""
    def __init__(self):
        self.documents: Dict[str, Document] = {}
    
    def add_document(self, doc: Document):
        self.documents[doc.id] = doc
    
    def get_document(self, doc_id: str) -> Document:
        return self.documents.get(doc_id)