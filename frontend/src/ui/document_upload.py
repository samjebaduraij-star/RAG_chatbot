# document_upload.py
# Description: Document upload and processing UI component
# Dependencies: streamlit, pathlib, typing
# Author: AI Generated Code
# Created: August 09, 2025

import streamlit as st
import logging
from typing import List, Optional, Dict, Any
from pathlib import Path
import os

from ..core.document_processor import DocumentProcessor
from ..utils.file_utils import FileUtils
from ..utils.validators import FileValidator

class DocumentUpload:
    """Document upload component for the chatbot."""
    
    def __init__(self):
        """Initialize document upload component."""
        self.document_processor = DocumentProcessor()
        self.file_utils = FileUtils()
        self.validator = FileValidator()
        self.logger = logging.getLogger(__name__)
        
        # Supported file types
        self.supported_types = ["pdf", "docx", "txt", "csv"]
        self.max_file_size = int(os.getenv("MAX_FILE_SIZE_MB", "50")) * 1024 * 1024
    
    def render(self) -> Optional[List]:
        """Render document upload interface.
        
        Returns:
            List of uploaded files or None
        """
        try:
            # File upload widget
            uploaded_files = st.file_uploader(
                label="Upload Documents",
                type=self.supported_types,
                accept_multiple_files=True,
                help=f"Supported formats: {', '.join([ext.upper() for ext in self.supported_types])}. Max size: {self.max_file_size // 1024 // 1024}MB per file"
            )
            
            if uploaded_files:
                self._display_uploaded_files(uploaded_files)
                return uploaded_files
            
            # Upload instructions
            self._render_upload_instructions()
            
            return None
            
        except Exception as e:
            self.logger.error(f"Document upload render error: {e}")
            st.error(f"Upload interface error: {e}")
            return None
    
    def _display_uploaded_files(self, files: List) -> None:
        """Display uploaded files information.
        
        Args:
            files: List of uploaded files
        """
        st.subheader(f"📁 Uploaded Files ({len(files)})")
        
        for file in files:
            with st.expander(f"📄 {file.name}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Type:** {file.type}")
                    st.write(f"**Size:** {self._format_file_size(file.size)}")
                
                with col2:
                    # Validation status
                    is_valid, message = self.validator.validate_file(file)
                    if is_valid:
                        st.success("✅ Valid")
                    else:
                        st.error(f"❌ {message}")
    
    def _render_upload_instructions(self) -> None:
        """Render upload instructions."""
        with st.expander("📝 Upload Instructions", expanded=False):
            st.markdown("""
            ### Supported File Types:
            - **PDF** (.pdf): Text documents, reports, research papers
            - **Word** (.docx): Microsoft Word documents
            - **Text** (.txt): Plain text files
            - **CSV** (.csv): Comma-separated data files
            
            ### File Requirements:
            - Maximum file size: 50MB
            - Multiple files can be uploaded simultaneously
            - Files are processed automatically after upload
            
            ### Processing Features:
            - Text extraction and chunking
            - Semantic search preparation
            - Metadata extraction
            - Local storage and indexing
            """)
    
    def process_file(self, file) -> bool:
        """Process uploaded file.
        
        Args:
            file: Uploaded file object
        
        Returns:
            True if processing successful, False otherwise
        """
        try:
            # Validate file
            is_valid, validation_message = self.validator.validate_file(file)
            if not is_valid:
                st.error(f"File validation failed: {validation_message}")
                return False
            
            # Save file temporarily
            temp_path = self._save_temp_file(file)
            if not temp_path:
                return False
            
            # Process document
            success = self.document_processor.process_document(
                file_path=temp_path,
                original_filename=file.name,
                file_type=file.type
            )
            
            # Clean up temp file
            self._cleanup_temp_file(temp_path)
            
            return success
            
        except Exception as e:
            self.logger.error(f"File processing error: {e}")
            st.error(f"Error processing file {file.name}: {e}")
            return False
    
    def _save_temp_file(self, file) -> Optional[Path]:
        """Save uploaded file temporarily.
        
        Args:
            file: Uploaded file object
        
        Returns:
            Path to temporary file or None if failed
        """
        try:
            # Create temp directory
            temp_dir = Path("frontend/data/uploads/temp")
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename
            temp_path = temp_dir / f"temp_{file.name}"
            
            # Write file content
            with open(temp_path, "wb") as f:
                f.write(file.getbuffer())
            
            return temp_path
            
        except Exception as e:
            self.logger.error(f"Error saving temp file: {e}")
            return None
    
    def _cleanup_temp_file(self, file_path: Path) -> None:
        """Clean up temporary file.
        
        Args:
            file_path: Path to temporary file
        """
        try:
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            self.logger.error(f"Error cleaning temp file: {e}")
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format.
        
        Args:
            size_bytes: File size in bytes
        
        Returns:
            Formatted file size string
        """
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f}{size_names[i]}"
    
    def get_processed_documents(self) -> List[Dict[str, Any]]:
        """Get list of processed documents.
        
        Returns:
            List of processed document metadata
        """
        try:
            return self.document_processor.get_processed_documents()
        except Exception as e:
            self.logger.error(f"Error getting processed documents: {e}")
            return []