"""DOCX document parser."""

import io
from pathlib import Path
from typing import Dict, Any, Tuple
from docx import Document

from src.utils import get_logger

logger = get_logger()


class DOCXParser:
    """
    DOCX document parser.
    
    Extracts text from Microsoft Word documents (.docx, .doc).
    """
    
    def __init__(self):
        """Initialize DOCX parser."""
        logger.debug("DOCXParser initialized")
    
    def parse_file(self, file_path: Path) -> Tuple[str, Dict[str, Any]]:
        """
        Parse DOCX from file path.
        
        Args:
            file_path: Path to DOCX file
            
        Returns:
            Tuple of (extracted_text, metadata)
        """
        logger.info(f"Parsing DOCX file: {file_path}")
        
        try:
            doc = Document(file_path)
            return self._extract_content(doc)
        except Exception as e:
            logger.error(f"Error parsing DOCX file: {str(e)}")
            raise
    
    def parse_bytes(self, file_bytes: bytes) -> Tuple[str, Dict[str, Any]]:
        """
        Parse DOCX from bytes.
        
        Args:
            file_bytes: DOCX file bytes
            
        Returns:
            Tuple of (extracted_text, metadata)
        """
        logger.info("Parsing DOCX from bytes")
        
        try:
            doc = Document(io.BytesIO(file_bytes))
            return self._extract_content(doc)
        except Exception as e:
            logger.error(f"Error parsing DOCX bytes: {str(e)}")
            raise
    
    def _extract_content(self, doc: Document) -> Tuple[str, Dict[str, Any]]:
        """
        Extract text and metadata from Document object.
        
        Args:
            doc: python-docx Document object
            
        Returns:
            Tuple of (extracted_text, metadata)
        """
        text_parts = []
        
        # Extract paragraphs
        for para in doc.paragraphs:
            if para.text.strip():
                text_parts.append(para.text)
        
        # Extract tables
        for table in doc.tables:
            table_text = self._extract_table_text(table)
            if table_text:
                text_parts.append(table_text)
        
        full_text = "\n".join(text_parts)
        
        # Extract metadata
        metadata = {
            'paragraph_count': len(doc.paragraphs),
            'table_count': len(doc.tables),
            'parser': 'python-docx'
        }
        
        # Extract core properties if available
        try:
            core_props = doc.core_properties
            metadata.update({
                'title': core_props.title or '',
                'author': core_props.author or '',
                'subject': core_props.subject or '',
                'keywords': core_props.keywords or '',
                'created': str(core_props.created) if core_props.created else '',
                'modified': str(core_props.modified) if core_props.modified else ''
            })
        except Exception as e:
            logger.warning(f"Could not extract core properties: {str(e)}")
        
        logger.info(
            f"Extracted {len(full_text)} characters, "
            f"{metadata['paragraph_count']} paragraphs, "
            f"{metadata['table_count']} tables"
        )
        
        return full_text, metadata
    
    def _extract_table_text(self, table) -> str:
        """
        Extract text from a table.
        
        Args:
            table: python-docx Table object
            
        Returns:
            Formatted table text
        """
        table_lines = []
        
        for row in table.rows:
            cells = []
            for cell in row.cells:
                cell_text = cell.text.strip()
                if cell_text:
                    cells.append(cell_text)
            
            if cells:
                table_lines.append(" | ".join(cells))
        
        return "\n".join(table_lines) if table_lines else ""
