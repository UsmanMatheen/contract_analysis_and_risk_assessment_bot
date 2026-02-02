"""Main document parser for handling PDF, DOCX, and TXT files."""

import io
import re
from pathlib import Path
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
from langdetect import detect, LangDetectException

from .pdf_parser import PDFParser
from .docx_parser import DOCXParser
from .txt_parser import TXTParser
from .text_cleaner import TextCleaner
from config.settings import get_settings
from src.utils import get_logger

logger = get_logger()


@dataclass
class ParsedDocument:
    """Container for parsed document information."""
    
    text: str
    metadata: Dict[str, Any]
    language: str
    file_type: str
    page_count: Optional[int] = None
    word_count: int = 0
    char_count: int = 0
    is_valid: bool = True
    error_message: Optional[str] = None
    
    def __post_init__(self):
        """Calculate derived fields."""
        if self.text:
            self.word_count = len(self.text.split())
            self.char_count = len(self.text)


class DocumentParser:
    """
    Main document parser supporting PDF, DOCX, and TXT files.
    
    Features:
    - Multi-format support (PDF, DOCX, TXT)
    - Language detection (English, Hindi)
    - Text cleaning and normalization
    - Metadata extraction
    - Comprehensive error handling
    """
    
    def __init__(self):
        """Initialize document parser."""
        self.settings = get_settings()
        self.pdf_parser = PDFParser()
        self.docx_parser = DOCXParser()
        self.txt_parser = TXTParser()
        self.text_cleaner = TextCleaner()
        
        logger.info("DocumentParser initialized")
    
    def parse(
        self,
        file_path: Optional[Union[str, Path]] = None,
        file_bytes: Optional[bytes] = None,
        filename: Optional[str] = None
    ) -> ParsedDocument:
        """
        Parse document from file path or bytes.
        
        Args:
            file_path: Path to document file
            file_bytes: Document bytes (for uploaded files)
            filename: Original filename (required if using file_bytes)
            
        Returns:
            ParsedDocument with extracted text and metadata
            
        Raises:
            ValueError: If neither file_path nor file_bytes provided
            ValueError: If file type not supported
        """
        try:
            # Validate input
            if file_path is None and file_bytes is None:
                raise ValueError("Either file_path or file_bytes must be provided")
            
            if file_bytes and not filename:
                raise ValueError("filename required when using file_bytes")
            
            # Determine file type
            if file_path:
                file_path = Path(file_path)
                file_ext = file_path.suffix.lower().lstrip('.')
                filename = file_path.name
            else:
                file_ext = Path(filename).suffix.lower().lstrip('.')
            
            # Validate file extension
            if file_ext not in self.settings.ALLOWED_EXTENSIONS:
                raise ValueError(
                    f"Unsupported file type: {file_ext}. "
                    f"Allowed: {', '.join(self.settings.ALLOWED_EXTENSIONS)}"
                )
            
            logger.info(f"Parsing document: {filename} (type: {file_ext})")
            
            # Parse based on file type
            if file_ext == 'pdf':
                raw_text, metadata = self._parse_pdf(file_path, file_bytes)
            elif file_ext in ['docx', 'doc']:
                raw_text, metadata = self._parse_docx(file_path, file_bytes)
            elif file_ext == 'txt':
                raw_text, metadata = self._parse_txt(file_path, file_bytes)
            else:
                raise ValueError(f"Unsupported file extension: {file_ext}")
            
            # Clean text
            cleaned_text = self.text_cleaner.clean(raw_text)
            
            # Detect language
            language = self._detect_language(cleaned_text)
            
            # Create parsed document
            parsed_doc = ParsedDocument(
                text=cleaned_text,
                metadata={
                    **metadata,
                    'filename': filename,
                    'original_length': len(raw_text),
                    'cleaned_length': len(cleaned_text)
                },
                language=language,
                file_type=file_ext,
                page_count=metadata.get('page_count')
            )
            
            # Validate minimum content
            if parsed_doc.word_count < 10:
                logger.warning(f"Document has insufficient content: {parsed_doc.word_count} words")
                parsed_doc.is_valid = False
                parsed_doc.error_message = "Document appears to be empty or has insufficient text"
            
            logger.info(
                f"Document parsed successfully: {parsed_doc.word_count} words, "
                f"{parsed_doc.page_count or 'N/A'} pages, language: {language}"
            )
            
            return parsed_doc
            
        except Exception as e:
            logger.error(f"Error parsing document: {str(e)}")
            return ParsedDocument(
                text="",
                metadata={'error': str(e), 'filename': filename or 'unknown'},
                language="unknown",
                file_type=file_ext if 'file_ext' in locals() else "unknown",
                is_valid=False,
                error_message=str(e)
            )
    
    def _parse_pdf(
        self,
        file_path: Optional[Path],
        file_bytes: Optional[bytes]
    ) -> tuple[str, Dict[str, Any]]:
        """Parse PDF document."""
        if file_path:
            return self.pdf_parser.parse_file(file_path)
        else:
            return self.pdf_parser.parse_bytes(file_bytes)
    
    def _parse_docx(
        self,
        file_path: Optional[Path],
        file_bytes: Optional[bytes]
    ) -> tuple[str, Dict[str, Any]]:
        """Parse DOCX document."""
        if file_path:
            return self.docx_parser.parse_file(file_path)
        else:
            return self.docx_parser.parse_bytes(file_bytes)
    
    def _parse_txt(
        self,
        file_path: Optional[Path],
        file_bytes: Optional[bytes]
    ) -> tuple[str, Dict[str, Any]]:
        """Parse TXT document."""
        if file_path:
            return self.txt_parser.parse_file(file_path)
        else:
            return self.txt_parser.parse_bytes(file_bytes)
    
    def _detect_language(self, text: str) -> str:
        """
        Detect document language.
        
        Args:
            text: Document text
            
        Returns:
            Language code ('en', 'hi', or 'unknown')
        """
        try:
            # Use first 1000 characters for detection
            sample = text[:1000]
            
            if not sample.strip():
                return "unknown"
            
            detected = detect(sample)
            
            # Map detected language to supported languages
            if detected in ['en']:
                return 'en'
            elif detected in ['hi']:
                return 'hi'
            else:
                # Check for Hindi characters (Devanagari script)
                if self._contains_devanagari(sample):
                    return 'hi'
                return 'en'  # Default to English
                
        except LangDetectException:
            logger.warning("Language detection failed, defaulting to English")
            return 'en'
        except Exception as e:
            logger.error(f"Error in language detection: {str(e)}")
            return 'unknown'
    
    def _contains_devanagari(self, text: str) -> bool:
        """Check if text contains Devanagari (Hindi) script."""
        # Unicode range for Devanagari: U+0900 to U+097F
        devanagari_pattern = re.compile(r'[\u0900-\u097F]')
        return bool(devanagari_pattern.search(text))
    
    def validate_file_size(self, file_size_bytes: int) -> bool:
        """
        Validate file size against maximum allowed.
        
        Args:
            file_size_bytes: File size in bytes
            
        Returns:
            True if file size is acceptable
        """
        max_size = self.settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        return file_size_bytes <= max_size
    
    def get_supported_formats(self) -> list[str]:
        """Get list of supported file formats."""
        return self.settings.ALLOWED_EXTENSIONS
