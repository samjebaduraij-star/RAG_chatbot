# sidebar.py
# Description: Streamlit sidebar component for navigation and settings
# Dependencies: streamlit, typing, logging
# Author: AI Generated Code
# Created: August 12, 2025

import streamlit as st
import logging
from typing import Dict, Any, Optional
import os
from datetime import datetime

from ..services.gemini_client import GeminiClient
from ..core.history_manager import HistoryManager

class Sidebar:
    """Sidebar component for navigation and application settings."""
    
    def __init__(self):
        """Initialize sidebar component."""
        self.logger = logging.getLogger(__name__)
        self.gemini_client = GeminiClient()
        self.history_manager = HistoryManager()
    
    def render(self) -> None:
        """Render sidebar content."""
        try:
            with st.sidebar:
                self._render_header()
                self._render_api_status()
                self._render_session_info()
                self._render_settings()
                self._render_history_management()
                self._render_system_info()
                
        except Exception as e:
            self.logger.error(f"Sidebar render error: {e}")
            st.sidebar.error(f"Sidebar error: {e}")
    
    def _render_header(self) -> None:
        """Render sidebar header."""
        st.title("🤖 Q&A Chatbot")
        st.markdown("---")
        
        # App version and status
        st.markdown("""
        **Version:** 1.0.0  
        **Status:** 🟢 Online  
        **Model:** Gemini 2.5 Pro
        """)
        
        st.markdown("---")
    
    def _render_api_status(self) -> None:
        """Render API connection status."""
        st.subheader("🔌 API Status")
        
        # Test API connection button
        if st.button("Test Connection", help="Test Gemini API connection"):
            with st.spinner("Testing connection..."):
                result = self.gemini_client.test_connection()
                
                if result["success"]:
                    st.success("✅ API Connected")
                    st.caption(f"Response time: {result.get('response_time', 0):.2f}s")
                else:
                    st.error("❌ API Connection Failed")
                    st.caption(f"Error: {result.get('error', 'Unknown')}")
        
        # Display current model info
        with st.expander("Model Information", expanded=False):
            model_info = self.gemini_client.get_model_info()
            st.json(model_info)
        
        st.markdown("---")
    
    def _render_session_info(self) -> None:
        """Render current session information."""
        st.subheader("📊 Session Info")
        
        session_id = st.session_state.get("chat_session_id", "None")
        user_id = st.session_state.get("user_id", "default_user")
        message_count = len(st.session_state.get("messages", []))
        document_count = len(st.session_state.get("processed_documents", []))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Messages", message_count)
            st.metric("Documents", document_count)
        
        with col2:
            st.metric("User ID", user_id)
            st.caption(f"Session: {session_id[:8]}...")
        
        st.markdown("---")
    
    def _render_settings(self) -> None:
        """Render application settings."""
        st.subheader("⚙️ Settings")
        
        # Chat settings
        with st.expander("Chat Settings"):
            # Temperature setting
            temperature = st.slider(
                "Response Creativity",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Higher values make responses more creative"
            )
            
            # Max tokens
            max_tokens = st.slider(
                "Max Response Length",
                min_value=256,
                max_value=4096,
                value=2048,
                step=256,
                help="Maximum tokens in AI response"
            )
            
            # Context length
            context_length = st.slider(
                "Context History",
                min_value=1,
                max_value=20,
                value=5,
                step=1,
                help="Number of previous messages to include"
            )
            
            # Update session state
            st.session_state.update({
                "temperature": temperature,
                "max_tokens": max_tokens,
                "context_length": context_length
            })
        
        # Document settings
        with st.expander("Document Settings"):
            chunk_size = st.slider(
                "Document Chunk Size",
                min_value=500,
                max_value=2000,
                value=1000,
                step=100,
                help="Size of document chunks for processing"
            )
            
            similarity_threshold = st.slider(
                "Similarity Threshold",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.05,
                help="Minimum similarity for relevant documents"
            )
            
            st.session_state.update({
                "chunk_size": chunk_size,
                "similarity_threshold": similarity_threshold
            })
        
        st.markdown("---")
    
    def _render_history_management(self) -> None:
        """Render chat history management."""
        st.subheader("📚 History Management")
        
        # Load previous sessions
        sessions = self.history_manager.get_session_list()
        
        if sessions:
            selected_session = st.selectbox(
                "Load Previous Session",
                options=["Current Session"] + sessions,
                help="Select a previous chat session to load"
            )
            
            if selected_session != "Current Session":
                if st.button("Load Session"):
                    self._load_session(selected_session)
        
        # History statistics
        with st.expander("History Statistics"):
            stats = self.history_manager.get_statistics()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Sessions", stats.get("total_sessions", 0))
                st.metric("Total Messages", stats.get("total_messages", 0))
            
            with col2:
                st.metric("Avg Messages/Session", stats.get("avg_messages", 0))
                st.metric("Total Documents", stats.get("total_documents", 0))
        
        # Cleanup options
        with st.expander("Cleanup Options"):
            st.warning("⚠️ These actions cannot be undone!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Clear Old Sessions", help="Remove sessions older than 30 days"):
                    self._cleanup_old_sessions()
            
            with col2:
                if st.button("Reset All Data", help="Clear all chat history"):
                    self._reset_all_data()
        
        st.markdown("---")
    
    def _render_system_info(self) -> None:
        """Render system information."""
        st.subheader("💻 System Info")
        
        with st.expander("Application Details"):
            info = {
                "Python Version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
                "Streamlit Version": st.__version__,
                "Current Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Debug Mode": os.getenv("DEBUG", "false"),
                "Log Level": os.getenv("LOG_LEVEL", "INFO"),
                "Upload Folder": os.getenv("UPLOAD_FOLDER", "frontend/data/uploads"),
                "Max File Size": f"{os.getenv('MAX_FILE_SIZE_MB', '50')}MB"
            }
            
            for key, value in info.items():
                st.text(f"{key}: {value}")
        
        # Resource usage
        with st.expander("Resource Usage"):
            try:
                import psutil
                cpu_percent = psutil.cpu_percent()
                memory_percent = psutil.virtual_memory().percent
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("CPU Usage", f"{cpu_percent}%")
                with col2:
                    st.metric("Memory Usage", f"{memory_percent}%")
                    
            except ImportError:
                st.caption("Install psutil for resource monitoring")
    
    def _load_session(self, session_id: str) -> None:
        """Load a previous chat session.
        
        Args:
            session_id: Session identifier to load
        """
        try:
            messages = self.history_manager.load_session(session_id)
            st.session_state.messages = messages
            st.session_state.chat_session_id = session_id
            st.success(f"Loaded session: {session_id}")
            st.rerun()
            
        except Exception as e:
            self.logger.error(f"Error loading session: {e}")
            st.error(f"Failed to load session: {e}")
    
    def _cleanup_old_sessions(self) -> None:
        """Clean up old chat sessions."""
        try:
            removed_count = self.history_manager.cleanup_old_sessions(days=30)
            st.success(f"Removed {removed_count} old sessions")
            
        except Exception as e:
            self.logger.error(f"Error cleaning up sessions: {e}")
            st.error(f"Cleanup failed: {e}")
    
    def _reset_all_data(self) -> None:
        """Reset all application data."""
        try:
            # Confirm action
            if st.button("Confirm Reset", type="primary"):
                self.history_manager.reset_all_data()
                st.session_state.clear()
                st.success("All data has been reset")
                st.rerun()
                
        except Exception as e:
            self.logger.error(f"Error resetting data: {e}")
            st.error(f"Reset failed: {e}")