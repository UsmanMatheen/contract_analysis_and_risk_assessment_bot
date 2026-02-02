"""PDF document parser with multiple extraction strategies."""

import io
from pathlib import Path
from typing import Dict, Any, Tuple
import PyPDF2
import pdfplumber

from src.utils import get_logger

logger = get_logger()


class PDFParser:
    """
    PDF parser with fallback strategies.
    
    Uses multiple libraries to handle various PDF formats:
    1. pdfplumber - Best for complex layouts and tables
    2. PyPDF2 - Fallback for standard PDFs
    """
    
    def __init__(self):
        """Initialize PDF parser."""
        logger.debug("PDFParser initialized")
    
    def parse_file(self, file_path: Path) -> Tuple[str, Dict[str, Any]]:
        """
        Parse PDF from file path.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Tuple of (extracted_text, metadata)
        """
        logger.info(f"Parsing PDF file: {file_path}")
        
        try:
            # Try pdfplumber first (better extraction)
            text, metadata = self._parse_with_pdfplumber(file_path=file_path)
            
            if not text or len(text.strip()) < 100:
                logger.warning("pdfplumber extraction insufficient, trying PyPDF2")
                text, metadata = self._parse_with_pypdf2(file_path=file_path)
            
            return text, metadata
            
        except Exception as e:
            logger.error(f"Error parsing PDF file: {str(e)}")
            raise
    
    def parse_bytes(self, file_bytes: bytes) -> Tuple[str, Dict[str, Any]]:
        """
        Parse PDF from bytes.
        
        Args:
            file_bytes: PDF file bytes
            
        Returns:
            Tuple of (extracted_text, metadata)
        """
        logger.info("Parsing PDF from bytes")
        
        try:
            # Try pdfplumber first
            text, metadata = self._parse_with_pdfplumber(file_bytes=file_bytes)
            
            if not text or len(text.strip()) < 100:
                logger.warning("pdfplumber extraction insufficient, trying PyPDF2")
                text, metadata = self._parse_with_pypdf2(file_bytes=file_bytes)
            
            return text, metadata
            
        except Exception as e:
            logger.error(f"Error parsing PDF bytes: {str(e)}")
            raise
    
    def _parse_with_pdfplumber(
        self,
        file_path: Path = None,
        file_bytes: bytes = None
    ) -> Tuple[str, Dict[str, Any]]:
        """Parse PDF using pdfplumber."""
        text_parts = []
        metadata = {}
        
        try:
            # Open PDF
            if file_path:
                pdf = pdfplumber.open(file_path)
            else:
                pdf = pdfplumber.open(io.BytesIO(file_bytes))
            
            # Extract metadata
            metadata = {
                'page_count': len(pdf.pages),
                'parser': 'pdfplumber'
            }
            
            # Add PDF metadata if available
            if pdf.metadata:
                metadata.update({
                    'title': pdf.metadata.get('Title', ''),
                    'author': pdf.metadata.get('Author', ''),
                    'subject': pdf.metadata.get('Subject', ''),
                    'creator': pdf.metadata.get('Creator', ''),
                    'producer': pdf.metadata.get('Producer', ''),
                    'creation_date': pdf.metadata.get('CreationDate', '')
                })
            
            # Extract text from each page
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
                        logger.debug(f"Extracted {len(page_text)} chars from page {page_num}")
                except Exception as e:
                    logger.warning(f"Error extracting page {page_num}: {str(e)}")
                    continue
            
            pdf.close()
            
            full_text = "\n\n".join(text_parts)
            logger.info(f"pdfplumber extracted {len(full_text)} characters from {metadata['page_count']} pages")
            
            return full_text, metadata
            
        except Exception as e:
            logger.error(f"pdfplumber parsing failed: {str(e)}")
            raise
    
    def _parse_with_pypdf2(
        self,
        file_path: Path = None,
        file_bytes: bytes = None
    ) -> Tuple[str, Dict[str, Any]]:
        """Parse PDF using PyPDF2 (fallback)."""
        text_parts = []
        metadata = {}
        
        try:
            # Open PDF
            if file_path:
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    page_count = len(pdf_reader.pages)
                    pdf_metadata = pdf_reader.metadata
                    
                    # Extract text from each page
                    for page_num in range(page_count):
                        try:
                            page = pdf_reader.pages[page_num]
                            page_text = page.extract_text()
                            if page_text:
                                text_parts.append(page_text)
                        except Exception as e:
                            logger.warning(f"Error extracting page {page_num + 1}: {str(e)}")
                            continue
            else:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                page_count = len(pdf_reader.pages)
                pdf_metadata = pdf_reader.metadata
                
                # Extract text from each page
                for page_num in range(page_count):
                    try:
                        page = pdf_reader.pages[page_num]
                        page_text = page.extract_text()
                        if page_text:
                            text_parts.append(page_text)
                    except Exception as e:
                        logger.warning(f"Error extracting page {page_num + 1}: {str(e)}")
                        continue
            
            # Build metadata
            metadata = {
                'page_count': page_count,
                'parser': 'pypdf2'
            }
            
            if pdf_metadata:
                metadata.update({
                    'title': pdf_metadata.get('/Title', ''),
                    'author': pdf_metadata.get('/Author', ''),
                    'subject': pdf_metadata.get('/Subject', ''),
                    'creator': pdf_metadata.get('/Creator', ''),
                    'producer': pdf_metadata.get('/Producer', '')
                })
            
            full_text = "\n\n".join(text_parts)
            logger.info(f"PyPDF2 extracted {len(full_text)} characters from {page_count} pages")
            
            return full_text, metadata
            
        except Exception as e:
            logger.error(f"PyPDF2 parsing failed: {str(e)}")
            raise
