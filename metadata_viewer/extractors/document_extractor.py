# Document metadata extractor

from pathlib import Path
from typing import Dict, Any
from .base_extractor import BaseExtractor

try:
    from PyPDF2 import PdfReader
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False


class DocumentExtractor(BaseExtractor):
    # Extract metadata from document files

    def extract(self) -> Dict[str, Any]:
        # Extract document metadata

        metadata = {}

        extension = self.file_path.suffix.lower()

        if extension == '.pdf':
            metadata.update(self._extract_pdf())
        elif extension == '.txt':
            metadata.update(self._extract_text())
        else:
            metadata["Note"] = f"Limited support for {extension} files"

        return metadata
    
    def _extract_pdf(self) -> Dict[str, Any]:
        # Extract PDF metadata
        metadata = {}

        if not PYPDF2_AVAILABLE:
            metadata["Error"] = "PyPDF2 not available"
            return metadata
        
        try:
            with open(self.file_path, 'rb') as file:
                pdf = PdfReader(file)

                # Basic PDF info
                metadata["Pages"] = len(pdf.pages)

                # Pdf metadata extract
                if pdf.metadata:
                    info = pdf.metadata

                    # Common PDF metadata fields using property access
                    if info.title:
                        metadata["Title"] = str(info.title)
                    if info.author:
                        metadata["Author"] = str(info.author)
                    if info.subject:
                        metadata["Subject"] = str(info.subject)
                    if info.creator:
                        metadata["Creator"] = str(info.creator)
                    if info.producer:
                        metadata["Producer"] = str(info.producer)
                    if info.creation_date:
                        metadata["Creation Date"] = str(info.creation_date)
                    if info.modification_date:
                        metadata["Modification Date"] = str(info.modification_date)

                # Check if PDF is encrypted
                metadata["Encrypted"] = pdf.is_encrypted

                # Try to extract text length from the first page
                try:
                    first_page = pdf.pages[0]
                    text = first_page.extract_text()
                    if text:
                        metadata["First Page Characters"] = len(text)
                except Exception:
                    pass

        except Exception as e:
            metadata["Error"] = f"Failed to extract PDF metadata: {str(e)}"

        return metadata
    
    def _extract_text(self) -> Dict[str, Any]:
        # Extract text file metadata

        metadata = {}

        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()

                metadata["Characters"] = len(content)
                metadata["Lines"] = content.count('\n') + 1

                words = content.split()
                metadata["Words"] = len(words)

                # Detect encoding
                import codecs
                with open(self.file_path, 'rb') as f:
                    raw = f.read(4096)

                    # Try to detect BOM
                    if raw.startswith(codecs.BOM_UTF8):
                        metadata["Encoding"] = "UTF-8 with BOM"
                    elif raw.startswith(codecs.BOM_UTF16_LE):
                        metadata["Encoding"] = "UTF-16 LE with BOM"
                    elif raw.startswith(codecs.BOM_UTF16_BE):
                        metadata["Encoding"] = "UTF-16 BE with BOM"
                    else:
                        metadata["Encoding"] = "UTF-8 (assumed)"

        except UnicodeDecodeError:
            metadata["Encoding"] = "Binary or non-UTF-8"
        except Exception as e:
            metadata["Error"] = f"Failed to extract text metadata: {str(e)}"

        return metadata
    
    @staticmethod
    def _clean_pdf_date(date_str: str) -> str:
        # Clean a PDF date string

        # PDF Dates are in a format of D:YYYYMMDDHHmmSSOHH'mm'
        if date_str.startswith('D:'):
            date_str = date_str[2:]

        # Try parsing
        try:
            if len(date_str) >= 14:
                year = date_str[0:4]
                month = date_str[4:6]
                day = date_str[6:8]
                hour = date_str[8:10]
                minute = date_str[10:12]
                second = date_str[12:14]
                return f"{year}-{month}-{day} {hour}:{minute}:{second}"
        except (IndexError, ValueError):
            pass

        return date_str
