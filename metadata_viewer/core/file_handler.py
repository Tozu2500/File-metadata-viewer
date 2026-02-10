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
    
    