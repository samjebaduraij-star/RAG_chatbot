# chat_manager.py
# Description: Core chat management logic and AI response generation
# Dependencies: logging, typing, datetime, asyncio
# Author: AI Generated Code
# Created: August 09, 2025

import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import os

from ..services.gemini_client import GeminiClient
from ..services.embedding_service import EmbeddingService
from ..core.document_processor import DocumentProcessor
from tenacity import RetryError

class ChatManager:
    """Manages chat interactions and AI responses."""
    
    def __init__(self):
        """Initialize chat manager."""
        self.logger = logging.getLogger(__name__)
        self.gemini_client = GeminiClient()
        self.embedding_service = EmbeddingService()
        self.document_processor = DocumentProcessor()
        
        # Chat configuration
        self.max_context_length = 4000
        self.max_history_messages = 10
        self.model_name = "gemini-2.5-pro"  # Default model name
    
    def get_response(
        self,
        message: str,
        session_id: str,
        user_id: str,
        context_documents: List = None
    ) -> Dict[str, Any]:
        """Get AI response to user message.
        
        Args:
            message: User input message
            session_id: Current chat session ID
            user_id: User identifier
            context_documents: List of relevant documents
        
        Returns:
            Response dictionary with content and metadata
        """
        try:
            self.logger.info(f"Processing message: {message[:50]}...")
            self.logger.info(f"Context documents provided: {len(context_documents) if context_documents else 0}")
            
            # Build context from documents
            context = self._build_context(message, context_documents)
            if (not context) and context_documents:
                # If documents exist but nothing relevant was found, avoid hallucinations
                self.logger.info("No relevant context found in uploaded documents; returning grounded fallback message")
                return {
                    "content": "I don't know based on the provided documents. Please try a more specific question that matches the document wording.",
                    "model_used": self.model_name,
                    "tokens_used": 0,
                    "confidence_score": 0.0,
                    "context_used": False,
                }
            
            # Get conversation history
            history = self._get_conversation_history(session_id, user_id)
            
            # Generate response
            response = self._generate_response(message, context, history)
            
            return {
                "content": response["content"],
                "model_used": response.get("model", "gemini-2.5-pro"),
                "tokens_used": response.get("tokens", 0),
                "confidence_score": response.get("confidence", 0.0),
                "context_used": len(context) > 0
            }
            
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            
            # Provide specific error messages based on error type
            if "retryerror" in str(e).lower() and "resourceexhausted" in str(e).lower():
                error_msg = "⚠️ API quota exhausted after retry attempts. Please wait 10-15 minutes before trying again."
            elif "quota" in str(e).lower() or "resource_exhausted" in str(e).lower():
                error_msg = "⚠️ API quota limit reached. Please wait a few minutes before trying again."
            elif "rate" in str(e).lower() or "429" in str(e):
                error_msg = "⏳ Too many requests. Please wait a moment before trying again."
            elif "api_key" in str(e).lower() or "invalid" in str(e).lower():
                error_msg = "🔑 API key issue. Please check your configuration."
            elif "network" in str(e).lower() or "connection" in str(e).lower():
                error_msg = "🌐 Network connection issue. Please check your internet connection."
            else:
                error_msg = f"❌ Error: {str(e)[:100]}..." if len(str(e)) > 100 else f"❌ Error: {str(e)}"
            
            return {
                "content": error_msg,
                "model_used": "error",
                "tokens_used": 0,
                "confidence_score": 0.0,
                "context_used": False
            }
    
    def _build_context(self, message: str, context_documents: List = None) -> str:
        """Build context from relevant documents.
        
        Args:
            message: User message
            context_documents: Available documents
        
        Returns:
            Context string for AI prompt
        """
        try:
            if not context_documents:
                self.logger.info("No context documents provided")
                return ""

            self.logger.info(f"Building context with {len(context_documents)} documents")

            # 1) Load full contents (including chunks) for the provided documents
            docs_with_chunks: List[Dict[str, Any]] = []
            for d in context_documents:
                try:
                    doc_id = d.get("id") or d.get("document_id")
                    if not doc_id:
                        continue
                    doc_content = self.document_processor.get_document_content(doc_id)
                    if doc_content and doc_content.get("chunks"):
                        # Ensure filename is present for citation
                        if "filename" not in doc_content and d.get("filename"):
                            doc_content["filename"] = d.get("filename")
                        docs_with_chunks.append(doc_content)
                except Exception as e:
                    self.logger.warning(f"Failed loading document content for context: {e}")

            # 2) Try semantic retrieval using embeddings (best quality)
            relevant_chunks: List[Dict[str, Any]] = []
            if docs_with_chunks:
                try:
                    relevant_chunks = self.embedding_service.find_similar_chunks(
                        query=message,
                        documents=docs_with_chunks,
                        top_k=5,
                    )
                    # Normalize shape to common format
                    relevant_chunks = [
                        {
                            "document_name": rc.get("source", "Unknown"),
                            "content": rc.get("content", ""),
                            "similarity": rc.get("similarity", 0.0),
                        }
                        for rc in relevant_chunks
                    ]
                except Exception as e:
                    self.logger.warning(f"Embedding-based retrieval failed, will fallback: {e}")

            # 3) Fallback to keyword similarity search if embeddings produced nothing
            if not relevant_chunks:
                self.logger.info("Falling back to keyword similarity search")
                relevant_chunks = self.document_processor.search_documents(message, limit=5)

            if not relevant_chunks:
                self.logger.info("No relevant chunks found")
                return ""

            # 4) Build grounded context with citations
            context_parts: List[str] = []
            context_parts.append("You MUST answer strictly using the following document context. If the answer is not in the context, say you don't know.")
            # Log which chunks are being used for traceability
            try:
                preview = [
                    {
                        "source": c.get("document_name", "Unknown"),
                        "similarity": float(c.get("similarity", 0.0)) if isinstance(c.get("similarity"), (int, float)) else None,
                        "snippet": (c.get("content", "")[:120] + "...") if len(c.get("content", "")) > 120 else c.get("content", "")
                    }
                    for c in relevant_chunks[:3]
                ]
                self.logger.info(f"Selected top chunks for context: {preview}")
            except Exception:
                pass

            for i, chunk in enumerate(relevant_chunks[:3]):  # Limit to 3 most relevant
                name = chunk.get('document_name', 'Unknown')
                sim = chunk.get('similarity')
                sim_txt = f" (similarity: {sim:.2f})" if isinstance(sim, (int, float)) else ""
                context_parts.append(f"\n=== Source {i+1}: {name}{sim_txt} ===")
                context_parts.append(chunk.get("content", ""))
            context_parts.append("\n=== End of context ===")

            context_string = "\n".join(context_parts)
            self.logger.info(f"Built context with {len(context_string)} characters")
            return context_string
            
        except Exception as e:
            self.logger.error(f"Error building context: {e}")
            return ""
    
    def _find_relevant_chunks(self, message: str, documents: List) -> List[Dict[str, Any]]:
        """Find relevant document chunks for the message.
        
        Args:
            message: User message
            documents: Available documents
        
        Returns:
            List of relevant document chunks
        """
        try:
            # Get semantic similarity
            relevant_chunks = self.embedding_service.find_similar_chunks(
                query=message,
                documents=documents,
                top_k=5
            )
            
            return relevant_chunks
            
        except Exception as e:
            self.logger.error(f"Error finding relevant chunks: {e}")
            return []
    
    def _get_conversation_history(self, session_id: str, user_id: str) -> List[Dict[str, str]]:
        """Get recent conversation history.
        
        Args:
            session_id: Session identifier
            user_id: User identifier
        
        Returns:
            List of recent messages
        """
        try:
            history_file = f"frontend/data/chat_history/{session_id}_history.json"
            
            if not os.path.exists(history_file):
                return []
            
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
            
            # Get recent messages
            recent_messages = history[-self.max_history_messages:]
            
            return [
                {
                    "role": msg["role"],
                    "content": msg["content"]
                }
                for msg in recent_messages
                if msg["role"] in ["user", "assistant"]
            ]
            
        except Exception as e:
            self.logger.error(f"Error getting conversation history: {e}")
            return []
    
    def _generate_response(
        self,
        message: str,
        context: str,
        history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Generate AI response using Gemini API.
        
        Args:
            message: User message
            context: Document context
            history: Conversation history
        
        Returns:
            AI response with metadata
        """
        try:
            # Build prompt
            prompt = self._build_prompt(message, context, history)
            
            # Get response from Gemini
            response = self.gemini_client.generate_response(prompt)
            
            return response
            
        except RetryError as e:
            self.logger.error(f"Retry failed after all attempts: {e}")
            return {
                "content": "⚠️ API quota limit reached after multiple retry attempts. Please wait a few minutes before trying again. Document processing is still available.",
                "model": self.model_name,
                "tokens": 0,
                "confidence": 0.0,
                "finish_reason": "retry_exhausted",
                "response_time": 0.0
            }
        except Exception as e:
            self.logger.error(f"Gemini API error: {e}")
            # Handle quota exceeded errors gracefully
            if "quota" in str(e).lower() or "resource_exhausted" in str(e).lower():
                return {
                    "content": "⚠️ API quota limit reached. Please try again later or upgrade your API plan. The system can still process documents and provide basic functionality.",
                    "model": self.model_name,
                    "tokens": 0,
                    "confidence": 0.0,
                    "finish_reason": "quota_exceeded",
                    "response_time": 0.0
                }
            raise
    
    def _build_prompt(
        self,
        message: str,
        context: str,
        history: List[Dict[str, str]]
    ) -> str:
        """Build comprehensive prompt for AI.
        
        Args:
            message: User message
            context: Document context
            history: Conversation history
        
        Returns:
            Complete prompt string
        """
        prompt_parts = []
        
        # System instruction
        prompt_parts.append("""You are an intelligent Q&A assistant. You help users by answering questions based on provided documents and context. Be helpful, accurate, and concise in your responses.

Instructions:
- Use ONLY the provided document context to answer. If the answer is not in the context, respond with: "I don't know based on the provided documents."
- Cite which source chunk you used when relevant (e.g., Source 1, Source 2).
- Be conversational and helpful.
- Provide specific answers with references to source material when possible.
""")
        
        # Add context if available
        if context:
            prompt_parts.append(f"\nContext from documents:\n{context}")
        
        # Add conversation history
        if history:
            prompt_parts.append("\nConversation history:")
            for msg in history[-5:]:  # Last 5 messages
                prompt_parts.append(f"{msg['role'].title()}: {msg['content']}")
        
        # Add current question
        prompt_parts.append(f"\nUser: {message}")
        prompt_parts.append("Assistant:")
        
        return "\n".join(prompt_parts)
    
    async def get_response_async(
        self,
        message: str,
        session_id: str,
        user_id: str,
        context_documents: List = None
    ) -> Dict[str, Any]:
        """Async version of get_response for concurrent processing.
        
        Args:
            message: User input message
            session_id: Current chat session ID
            user_id: User identifier
            context_documents: List of relevant documents
        
        Returns:
            Response dictionary with content and metadata
        """
        return await asyncio.to_thread(
            self.get_response,
            message,
            session_id,
            user_id,
            context_documents
        )