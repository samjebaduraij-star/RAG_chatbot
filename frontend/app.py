# app.py
# Description: Main Streamlit application entry point for the Q&A chatbot
# Dependencies: streamlit, python-dotenv, logging
# Author: AI Generated Code
# Created: August 09, 2025

import os
import sys
import streamlit as st
from pathlib import Path
from typing import Optional
import logging
from dotenv import load_dotenv

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv()

# Import application modules
from src.ui.chat_interface import ChatInterface
from src.ui.document_upload import DocumentUpload
from src.ui.sidebar import Sidebar
from src.core.chat_manager import ChatManager
from src.core.history_manager import HistoryManager
from src.config.logging_config import setup_logging

class QAChatbotApp:
    """Main application class for the Q&A Chatbot."""
    
    def __init__(self):
        """Initialize the chatbot application."""
        self.setup_logging()
        self.setup_page_config()
        self.initialize_components()
    
    def setup_logging(self) -> None:
        """Configure application logging."""
        setup_logging()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Starting Q&A Chatbot Application")
    
    def setup_page_config(self) -> None:
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title="Advanced Q&A Chatbot",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://github.com/your-repo/help',
                'Report a bug': "https://github.com/your-repo/issues",
                'About': "# Advanced Q&A Chatbot v1.0.0\nBuilt with Streamlit and Gemini AI"
            }
        )
    
    def initialize_components(self) -> None:
        """Initialize application components."""
        try:
            # Initialize core managers first
            self.history_manager = HistoryManager()
            
            # Initialize UI components (skip chat_manager for now to avoid API key issues)
            self.sidebar = None  # Will initialize later if API key is available
            self.document_upload = DocumentUpload()
            self.chat_interface = None  # Will initialize later if API key is available
            
            # Try to initialize chat manager and dependent components
            try:
                self.chat_manager = ChatManager()
                self.sidebar = Sidebar()
                self.chat_interface = ChatInterface(self.chat_manager, self.history_manager)
            except ValueError as api_error:
                self.logger.warning(f"API-dependent components not initialized: {api_error}")
                st.warning("⚠️ Please set your GEMINI_API_KEY in the .env file to enable AI chat features.")
            
            # Initialize session state
            self.initialize_session_state()
            
        except Exception as e:
            self.logger.error(f"Failed to initialize components: {e}")
            st.error(f"Application initialization failed: {e}")
    
    def initialize_session_state(self) -> None:
        """Initialize Streamlit session state variables."""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        if "chat_session_id" not in st.session_state:
            st.session_state.chat_session_id = self.history_manager.create_new_session()
        
        if "processed_documents" not in st.session_state:
            # Load existing processed documents on startup
            from src.core.document_processor import DocumentProcessor
            doc_processor = DocumentProcessor()
            st.session_state.processed_documents = doc_processor.get_processed_documents()
        
        if "user_id" not in st.session_state:
            st.session_state.user_id = "default_user"
    
    def run(self) -> None:
        """Run the main application."""
        try:
            # Display header
            st.title("🤖 Advanced Q&A Chatbot")
            st.markdown("---")
            
            # Create layout
            col1, col2 = st.columns([3, 1])
            
            with col2:
                # Sidebar content
                if self.sidebar:
                    self.sidebar.render()
                else:
                    st.subheader("⚙️ Settings")
                    st.info("API configuration required for full functionality")
                
                # Document upload section
                st.subheader("📄 Document Upload")
                uploaded_files = self.document_upload.render()
                
                if uploaded_files:
                    self.process_uploaded_files(uploaded_files)
            
            with col1:
                # Chat interface - move outside columns to avoid st.chat_input restriction
                pass
            
            # Chat interface outside columns
            if self.chat_interface:
                st.subheader("💬 Chat")
                self.chat_interface.render()
            else:
                st.subheader("💬 Chat")
                st.info("Please configure your GEMINI_API_KEY in the .env file to enable chat functionality.")
                st.code("GEMINI_API_KEY=your_actual_api_key_here", language="bash")
            
        except Exception as e:
            self.logger.error(f"Application runtime error: {e}")
            st.error(f"An error occurred: {e}")
    
    def process_uploaded_files(self, files: list) -> None:
        """Process uploaded files."""
        try:
            for file in files:
                # Always attempt processing; afterward refresh the processed docs list
                with st.spinner(f"Processing {file.name}..."):
                    success = self.document_upload.process_file(file)
                    if success:
                        # Refresh processed documents from persistent index
                        try:
                            st.session_state.processed_documents = self.document_upload.get_processed_documents()
                        except Exception:
                            pass
                        st.success(f"✅ Processed: {file.name}")
                    else:
                        st.error(f"❌ Failed to process: {file.name}")
        except Exception as e:
            self.logger.error(f"File processing error: {e}")
            st.error(f"Error processing files: {e}")

def main():
    """Main application entry point."""
    app = QAChatbotApp()
    app.run()

if __name__ == "__main__":
    main()