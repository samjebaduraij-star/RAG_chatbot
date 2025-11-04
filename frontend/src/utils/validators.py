# validators.py
# Description: Input validation helpers for files and user inputs
# Dependencies: typing, os
# Author: AI Generated Code
# Created: August 15, 2025

from typing import Any, Tuple
import os

class FileValidator:
    """Validates file uploads according to type and size."""
    def __init__(self):
        self.max_file_size = int(os.getenv("MAX_FILE_SIZE_MB", "50")) * 1024 * 1024
        self.allowed_extensions = os.getenv("ALLOWED_EXTENSIONS", "pdf,docx,txt,csv").split(',')
    
    def validate_file(self, file) -> Tuple[bool, str]:
        try:
            ext = file.name.split('.')[-1].lower()
            if ext not in self.allowed_extensions:
                return False, f"Extension '{ext}' is not allowed."
            if file.size > self.max_file_size:
                return False, f"File size exceeds {self.max_file_size//1024//1024}MB."
            return True, "File is valid."
        except Exception as e:
            return False, f"Validation error: {e}"