# File handling operations

from pathlib import Path
from typing import List, Optional
from utils.constants import ALL_SUPPORTED_EXTENSIONS

class FileHandler:
    # Handle file operations and filtering

    @staticmethod
    def is_supported(file_path: Path) -> bool:
        # Check if a file is supported.
        # Args: file_path: Path to file
        # Returns: True if file is supported
        return file_path.suffix.lower() in ALL_SUPPORTED_EXTENSIONS
    
    @staticmethod
    def get_file_type(file_path: Path) -> str:
        from utils.constants import (
            IMAGE_EXTENSIONS,
            VIDEO_EXTENSIONS,
            AUDIO_EXTENSIONS,
            DOCUMENT_EXTENSIONS
        )

        ext = file_path.suffix().lower()

        if ext in IMAGE_EXTENSIONS:
            return "image"
        elif ext in VIDEO_EXTENSIONS:
            return "video"
        elif ext in AUDIO_EXTENSIONS:
            return "audio"
        elif ext in DOCUMENT_EXTENSIONS:
            return "document"
        else:
            return "unknown"
        
    @staticmethod
    def scan_directory(directory: Path, recursive: bool = False) -> List[Path]:
        files = []

        try:
            if recursive:
                for item in directory.rglob('*'):
                    if item.is_file() and FileHandler.is_supported(item):
                        files.append(item)
            else:
                for item in directory.iterdir():
                    if item.is_file() and FileHandler.is_supported(item):
                        files.append(item)
        except PermissionError:
            pass  # Skipping directories without access to

        return sorted(files)
    
    @staticmethod
    def get_files_by_type(files: List[Path], file_type: str) -> List[Path]:
        
        return [f for f in files if FileHandler.get_file_type(f) == file_type]

