# Base class for extracting metadata
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any

class BaseExtractor(ABC):
    # Abstract base class for metadata extractors

    def __init__(self, file_path: Path):
        # Initialize the extractor with a file-path

        self.file_path = file_path
        self.metadata = {}

    @abstractmethod
    def extract(self) -> Dict[str, Any]:
        # Extract metadata from the file
        # Return a dictionary containing K-V pairs
        pass

    def _get_basic_info(self) -> Dict[str, Any]:
        # Get basic file information
        stat = self.file_path.stat()
        return {
            "File Name": self.file_path.name,
            "File Path": str(self.file_path.absolute()),
            "File Size": stat.st_size,
            "Created": stat.st_ctime,
            "Modified": stat.st_mtime,
            "Accessed": stat.st_atime,
        }
    
    def get_metadata(self) -> Dict[str, Any]:
        # Get all metadata including the basic info
        basic_info = self._get_basic_info()
        extracted_metadata = self.extract()

        return {**basic_info, **extracted_metadata}