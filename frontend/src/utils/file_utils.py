# file_utils.py
# Description: File handling and management utilities
# Dependencies: pathlib, shutil, os, hashlib
# Author: AI Generated Code
# Created: August 12, 2025

import os
import shutil
import hashlib
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import mimetypes
import tempfile
from datetime import datetime

class FileUtils:
    """Utility class for file operations and management."""
    
    def __init__(self):
        """Initialize file utilities."""
        self.logger = logging.getLogger(__name__)
        
        # Supported file types
        self.supported_extensions = {
            '.pdf': 'application/pdf',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.txt': 'text/plain',
            '.csv': 'text/csv'
        }
    
    def ensure_directory(self, directory_path: Path) -> bool:
        """Ensure directory exists, create if it doesn't.
        
        Args:
            directory_path: Path to directory
        
        Returns:
            True if directory exists or was created successfully
        """
        try:
            directory_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"Error creating directory {directory_path}: {e}")
            return False
    
    def get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """Get comprehensive file information.
        
        Args:
            file_path: Path to file
        
        Returns:
            Dictionary containing file information
        """
        try:
            if not file_path.exists():
                return {}
            
            stat_info = file_path.stat()
            
            info = {
                "name": file_path.name,
                "stem": file_path.stem,
                "suffix": file_path.suffix,
                "size_bytes": stat_info.st_size,
                "size_human": self.format_file_size(stat_info.st_size),
                "created": datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                "accessed": datetime.fromtimestamp(stat_info.st_atime).isoformat(),
                "is_file": file_path.is_file(),
                "is_dir": file_path.is_dir(),
                "absolute_path": str(file_path.absolute()),
                "mime_type": self.get_mime_type(file_path),
                "is_supported": self.is_supported_file(file_path)
            }
            
            # Add file hash for uniqueness
            if file_path.is_file():
                info["md5_hash"] = self.calculate_file_hash(file_path)
            
            return info
            
        except Exception as e:
            self.logger.error(f"Error getting file info for {file_path}: {e}")
            return {}
    
    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format.
        
        Args:
            size_bytes: Size in bytes
        
        Returns:
            Formatted size string
        """
        try:
            if size_bytes == 0:
                return "0 B"
            
            size_names = ["B", "KB", "MB", "GB", "TB"]
            i = 0
            size = float(size_bytes)
            
            while size >= 1024.0 and i < len(size_names) - 1:
                size /= 1024.0
                i += 1
            
            return f"{size:.1f} {size_names[i]}"
            
        except Exception as e:
            self.logger.error(f"Error formatting file size: {e}")
            return f"{size_bytes} B"
    
    def get_mime_type(self, file_path: Path) -> str:
        """Get MIME type of file.
        
        Args:
            file_path: Path to file
        
        Returns:
            MIME type string
        """
        try:
            # Check our supported extensions first
            if file_path.suffix.lower() in self.supported_extensions:
                return self.supported_extensions[file_path.suffix.lower()]
            
            # Use mimetypes module
            mime_type, _ = mimetypes.guess_type(str(file_path))
            return mime_type or "application/octet-stream"
            
        except Exception as e:
            self.logger.error(f"Error getting MIME type for {file_path}: {e}")
            return "application/octet-stream"
    
    def is_supported_file(self, file_path: Path) -> bool:
        """Check if file type is supported.
        
        Args:
            file_path: Path to file
        
        Returns:
            True if file type is supported
        """
        try:
            return file_path.suffix.lower() in self.supported_extensions
        except Exception:
            return False
    
    def calculate_file_hash(self, file_path: Path, algorithm: str = "md5") -> str:
        """Calculate hash of file content.
        
        Args:
            file_path: Path to file
            algorithm: Hash algorithm ('md5', 'sha1', 'sha256')
        
        Returns:
            Hex digest of file hash
        """
        try:
            hash_obj = hashlib.new(algorithm)
            
            with open(file_path, 'rb') as file:
                # Read file in chunks to handle large files
                for chunk in iter(lambda: file.read(8192), b""):
                    hash_obj.update(chunk)
            
            return hash_obj.hexdigest()
            
        except Exception as e:
            self.logger.error(f"Error calculating hash for {file_path}: {e}")
            return ""
    
    def copy_file(self, source: Path, destination: Path, overwrite: bool = False) -> bool:
        """Copy file from source to destination.
        
        Args:
            source: Source file path
            destination: Destination file path
            overwrite: Whether to overwrite existing files
        
        Returns:
            True if copy was successful
        """
        try:
            if not source.exists():
                self.logger.error(f"Source file does not exist: {source}")
                return False
            
            if destination.exists() and not overwrite:
                self.logger.warning(f"Destination file exists and overwrite=False: {destination}")
                return False
            
            # Ensure destination directory exists
            self.ensure_directory(destination.parent)
            
            # Copy file
            shutil.copy2(source, destination)
            
            self.logger.info(f"Successfully copied {source} to {destination}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error copying file from {source} to {destination}: {e}")
            return False
    
    def move_file(self, source: Path, destination: Path, overwrite: bool = False) -> bool:
        """Move file from source to destination.
        
        Args:
            source: Source file path
            destination: Destination file path
            overwrite: Whether to overwrite existing files
        
        Returns:
            True if move was successful
        """
        try:
            if not source.exists():
                self.logger.error(f"Source file does not exist: {source}")
                return False
            
            if destination.exists() and not overwrite:
                self.logger.warning(f"Destination file exists and overwrite=False: {destination}")
                return False
            
            # Ensure destination directory exists
            self.ensure_directory(destination.parent)
            
            # Move file
            shutil.move(str(source), str(destination))
            
            self.logger.info(f"Successfully moved {source} to {destination}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error moving file from {source} to {destination}: {e}")
            return False
    
    def delete_file(self, file_path: Path, force: bool = False) -> bool:
        """Delete file.
        
        Args:
            file_path: Path to file to delete
            force: Force deletion even if file is read-only
        
        Returns:
            True if deletion was successful
        """
        try:
            if not file_path.exists():
                return True  # Already deleted
            
            if force and file_path.is_file():
                # Remove read-only attribute if necessary
                file_path.chmod(0o777)
            
            if file_path.is_file():
                file_path.unlink()
            elif file_path.is_dir():
                shutil.rmtree(file_path)
            
            self.logger.info(f"Successfully deleted {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting {file_path}: {e}")
            return False
    
    def list_files(
        self,
        directory: Path,
        pattern: str = "*",
        recursive: bool = False,
        include_dirs: bool = False
    ) -> List[Path]:
        """List files in directory.
        
        Args:
            directory: Directory to search
            pattern: File pattern to match
            recursive: Search recursively
            include_dirs: Include directories in results
        
        Returns:
            List of matching file paths
        """
        try:
            if not directory.exists() or not directory.is_dir():
                return []
            
            if recursive:
                files = directory.rglob(pattern)
            else:
                files = directory.glob(pattern)
            
            result = []
            for file_path in files:
                if file_path.is_file() or (include_dirs and file_path.is_dir()):
                    result.append(file_path)
            
            return sorted(result)
            
        except Exception as e:
            self.logger.error(f"Error listing files in {directory}: {e}")
            return []
    
    def create_temp_file(self, suffix: str = "", prefix: str = "temp_") -> Path:
        """Create temporary file.
        
        Args:
            suffix: File suffix
            prefix: File prefix
        
        Returns:
            Path to temporary file
        """
        try:
            fd, temp_path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
            os.close(fd)  # Close file descriptor
            
            return Path(temp_path)
            
        except Exception as e:
            self.logger.error(f"Error creating temporary file: {e}")
            # Fallback
            temp_dir = Path(tempfile.gettempdir())
            return temp_dir / f"{prefix}{datetime.now().timestamp()}{suffix}"
    
    def create_temp_directory(self, prefix: str = "temp_") -> Path:
        """Create temporary directory.
        
        Args:
            prefix: Directory prefix
        
        Returns:
            Path to temporary directory
        """
        try:
            temp_path = tempfile.mkdtemp(prefix=prefix)
            return Path(temp_path)
            
        except Exception as e:
            self.logger.error(f"Error creating temporary directory: {e}")
            # Fallback
            temp_dir = Path(tempfile.gettempdir())
            fallback_dir = temp_dir / f"{prefix}{datetime.now().timestamp()}"
            self.ensure_directory(fallback_dir)
            return fallback_dir
    
    def clean_filename(self, filename: str) -> str:
        """Clean filename to remove invalid characters.
        
        Args:
            filename: Original filename
        
        Returns:
            Cleaned filename
        """
        try:
            # Remove invalid characters
            invalid_chars = '<>:"/\\|?*'
            cleaned = filename
            
            for char in invalid_chars:
                cleaned = cleaned.replace(char, '_')
            
            # Remove leading/trailing dots and spaces
            cleaned = cleaned.strip('. ')
            
            # Ensure filename is not empty
            if not cleaned:
                cleaned = "unnamed_file"
            
            # Limit length
            if len(cleaned) > 255:
                name, ext = os.path.splitext(cleaned)
                max_name_length = 255 - len(ext)
                cleaned = name[:max_name_length] + ext
            
            return cleaned
            
        except Exception as e:
            self.logger.error(f"Error cleaning filename: {e}")
            return "unnamed_file"
    
    def get_directory_size(self, directory: Path) -> int:
        """Get total size of directory.
        
        Args:
            directory: Directory path
        
        Returns:
            Total size in bytes
        """
        try:
            total_size = 0
            
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
            
            return total_size
            
        except Exception as e:
            self.logger.error(f"Error calculating directory size: {e}")
            return 0
    
    def compress_directory(self, directory: Path, output_path: Path) -> bool:
        """Compress directory to zip file.
        
        Args:
            directory: Directory to compress
            output_path: Output zip file path
        
        Returns:
            True if compression was successful
        """
        try:
            import zipfile
            
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in directory.rglob('*'):
                    if file_path.is_file():
                        # Calculate relative path
                        arcname = file_path.relative_to(directory)
                        zipf.write(file_path, arcname)
            
            self.logger.info(f"Successfully compressed {directory} to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error compressing directory: {e}")
            return False
    
    def extract_zip(self, zip_path: Path, extract_to: Path) -> bool:
        """Extract zip file to directory.
        
        Args:
            zip_path: Path to zip file
            extract_to: Directory to extract to
        
        Returns:
            True if extraction was successful
        """
        try:
            import zipfile
            
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                zipf.extractall(extract_to)
            
            self.logger.info(f"Successfully extracted {zip_path} to {extract_to}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error extracting zip file: {e}")
            return False
    
    def get_disk_usage(self, path: Path) -> Dict[str, int]:
        """Get disk usage statistics.
        
        Args:
            path: Path to check
        
        Returns:
            Dictionary with total, used, and free space in bytes
        """
        try:
            stat = shutil.disk_usage(path)
            
            return {
                "total": stat.total,
                "used": stat.used,
                "free": stat.free,
                "percent_used": round((stat.used / stat.total) * 100, 1)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting disk usage: {e}")
            return {"total": 0, "used": 0, "free": 0, "percent_used": 0}