# Main metadata extractor coordinator

from pathlib import Path
from typing import Dict, Any, Optional
from extractors import (
    ImageExtractor,
    VideoExtractor,
    AudioExtractor,
    DocumentExtractor,
)
from core.file_handler import FileHandler


class MetadataExtractor:
    # Coordinate metadata extraction for all the different file types

    def __init__(self):
        # Initialization
        self.extractors = {
            'image': ImageExtractor,
            'video': VideoExtractor,
            'audio': AudioExtractor,
            'document': DocumentExtractor
        }

    def extract(self, file_path: Path) -> Optional[Dict[str, Any]]:
        # Extract metadata from a file

        if not file_path.exists():
            return None
        
        file_type = FileHandler.get_file_type(file_path)

        if file_type == 'unknown':
            return self._get_basic_metadata(file_path)
        
        extractor_class = self.extractors.get(file_type)
        if not extractor_class:
            return self._get_basic_metadata(file_path)
        
        try:
            extractor = extractor_class(file_path)
            metadata = extractor.get_metadata()
            metadata['File Type'] = file_type.title()
            return metadata
        except Exception as e:
            metadata = self._get_basic_metadata(file_path)
            metadata['Extraction Error'] = str(e)
            return metadata
        
    def _get_basic_metadata(self, file_path: Path) -> Dict[str, Any]:
        # Get basic metadata for the unsupported file group
        stat = file_path.stat()
        return {
            "File Name": file_path.name,
            "File Path": str(file_path.absolute()),
            "File Type": "Unknown",
            "File Size": stat.st_size,
            "Created": stat.st_ctime,
            "Modified": stat.st_mtime,
            "Accessed": stat.st_atime,
        }
