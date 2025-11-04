# documents.py
# Description: FastAPI endpoints for documents
# Dependencies: backend/app/models/document_models.py
# Author: AI Generated Code
# Created: August 15, 2025

from fastapi import APIRouter, HTTPException
from backend.app.models.document_models import Document
from backend.app.services.document_service import DocumentService

router = APIRouter()
document_service = DocumentService()

@router.post("/documents")
async def upload_document(doc: Document):
    document_service.add_document(doc)
    return {"message": "Document uploaded", "document_id": doc.id}

@router.get("/documents/{doc_id}")
async def get_document(doc_id: str):
    doc = document_service.get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc