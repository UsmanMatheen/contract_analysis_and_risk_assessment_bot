"""Plain text document parser."""

import io
from pathlib import Path
from typing import Dict, Any, Tuple
import chardet

from src.utils import get_logger

logger = get_logger()


class TXTParser:
    """
    Plain text document parser.
    
    Handles various text encodings (UTF-8, Latin-1, etc.)
    """
    
    def __init__(self):
        """Initialize TXT parser."""
        logger.debug("TXTParser initialized")
    
    def parse_file(self, file_path: Path) -> Tuple[str, Dict[str, Any]]:
        """
        Parse TXT from file path.
        
        Args:
            file_path: Path to TXT file
            
        Returns:
            Tuple of (extracted_text, metadata)
        """
        logger.info(f"Parsing TXT file: {file_path}")
        
        try:
            # Read file bytes
            with open(file_path, 'rb') as f:
                file_bytes = f.read()
            
            return self._parse_text_bytes(file_bytes)
            
        except Exception as e:
            logger.error(f"Error parsing TXT file: {str(e)}")
            raise
    
    def parse_bytes(self, file_bytes: bytes) -> Tuple[str, Dict[str, Any]]:
        """
        Parse TXT from bytes.
        
        Args:
            file_bytes: TXT file bytes
            
        Returns:
            Tuple of (extracted_text, metadata)
        """
        logger.info("Parsing TXT from bytes")
        
        try:
            return self._parse_text_bytes(file_bytes)
        except Exception as e:
            logger.error(f"Error parsing TXT bytes: {str(e)}")
            raise
    
    def _parse_text_bytes(self, file_bytes: bytes) -> Tuple[str, Dict[str, Any]]:
        """
        Parse text bytes with encoding detection.
        
        Args:
            file_bytes: Text file bytes
            
        Returns:
            Tuple of (extracted_text, metadata)
        """
        # Detect encoding
        encoding_info = chardet.detect(file_bytes)
        encoding = encoding_info['encoding']
        confidence = encoding_info['confidence']
        
        logger.info(f"Detected encoding: {encoding} (confidence: {confidence:.2f})")
        
        # Try detected encoding first
        try:
            text = file_bytes.decode(encoding or 'utf-8')
        except (UnicodeDecodeError, TypeError):
            logger.warning(f"Failed to decode with {encoding}, trying UTF-8")
            try:
                text = file_bytes.decode('utf-8')
                encoding = 'utf-8'
            except UnicodeDecodeError:
                logger.warning("UTF-8 failed, trying Latin-1")
                text = file_bytes.decode('latin-1', errors='ignore')
                encoding = 'latin-1'
        
        # Count lines
        lines = text.splitlines()
        line_count = len(lines)
        non_empty_lines = len([line for line in lines if line.strip()])
        
        metadata = {
            'encoding': encoding,
            'encoding_confidence': confidence,
            'line_count': line_count,
            'non_empty_lines': non_empty_lines,
            'parser': 'chardet'
        }
        
        logger.info(
            f"Extracted {len(text)} characters, "
            f"{non_empty_lines}/{line_count} non-empty lines"
        )
        
        return text, metadata
