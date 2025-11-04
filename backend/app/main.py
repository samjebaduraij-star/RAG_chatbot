# main.py
# Description: FastAPI application entry point
# Dependencies: FastAPI, backend/app/api
# Author: AI Generated Code
# Created: August 15, 2025

from fastapi import FastAPI
from backend.app.api.chat import router as chat_router
from backend.app.api.documents import router as documents_router
from backend.app.api.history import router as history_router

app = FastAPI(title="Intelligent Q&A Chatbot Backend")

app.include_router(chat_router, prefix="/api")
app.include_router(documents_router, prefix="/api")
app.include_router(history_router, prefix="/api")