"""Text cleaning and normalization utilities."""

import re
from typing import Optional

from src.utils import get_logger

logger = get_logger()


class TextCleaner:
    """
    Text cleaning and normalization for contract documents.
    
    Handles:
    - Whitespace normalization
    - Special character handling
    - Line break normalization
    - Header/footer removal patterns
    - Page number removal
    """
    
    def __init__(self):
        """Initialize text cleaner."""
        logger.debug("TextCleaner initialized")
    
    def clean(self, text: str, aggressive: bool = False) -> str:
        """
        Clean and normalize text.
        
        Args:
            text: Raw text to clean
            aggressive: If True, apply more aggressive cleaning
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        logger.debug(f"Cleaning text: {len(text)} characters")
        
        # Basic cleaning
        cleaned = self._normalize_whitespace(text)
        cleaned = self._remove_page_numbers(cleaned)
        cleaned = self._normalize_line_breaks(cleaned)
        cleaned = self._remove_excessive_newlines(cleaned)
        
        if aggressive:
            cleaned = self._remove_headers_footers(cleaned)
            cleaned = self._remove_special_characters(cleaned)
        
        # Final cleanup
        cleaned = self._final_cleanup(cleaned)
        
        logger.debug(f"Cleaned text: {len(cleaned)} characters")
        
        return cleaned
    
    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace characters."""
        # Replace tabs with spaces
        text = text.replace('\t', ' ')
        
        # Replace multiple spaces with single space
        text = re.sub(r' {2,}', ' ', text)
        
        # Replace non-breaking spaces
        text = text.replace('\xa0', ' ')
        text = text.replace('\u200b', '')  # Zero-width space
        
        return text
    
    def _remove_page_numbers(self, text: str) -> str:
        """Remove common page number patterns."""
        # Pattern: "Page X", "Page X of Y", standalone numbers
        patterns = [
            r'Page\s+\d+\s*(?:of\s+\d+)?',
            r'^\s*\d+\s*$',  # Standalone numbers on a line
            r'\[Page\s+\d+\]',
            r'- \d+ -',  # Centered page numbers like "- 1 -"
        ]
        
        for pattern in patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)
        
        return text
    
    def _normalize_line_breaks(self, text: str) -> str:
        """Normalize line breaks."""
        # Replace Windows line breaks
        text = text.replace('\r\n', '\n')
        text = text.replace('\r', '\n')
        
        return text
    
    def _remove_excessive_newlines(self, text: str) -> str:
        """Remove excessive newlines (more than 2)."""
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text
    
    def _remove_headers_footers(self, text: str) -> str:
        """
        Remove common header/footer patterns.
        
        This is aggressive and may remove legitimate content.
        Use with caution.
        """
        # Common header patterns
        header_patterns = [
            r'^.*confidential.*$',
            r'^.*proprietary.*$',
            r'^.*\d{1,2}/\d{1,2}/\d{2,4}.*$',  # Dates at start of line
        ]
        
        for pattern in header_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)
        
        return text
    
    def _remove_special_characters(self, text: str) -> str:
        """
        Remove or replace special characters.
        
        Preserves characters important for contracts.
        """
        # Remove control characters except newlines
        text = ''.join(char for char in text if char.isprintable() or char == '\n')
        
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        # Normalize dashes
        text = text.replace('–', '-').replace('—', '-')
        
        return text
    
    def _final_cleanup(self, text: str) -> str:
        """Final cleanup pass."""
        # Trim lines
        lines = [line.strip() for line in text.split('\n')]
        
        # Remove empty lines from start and end
        while lines and not lines[0]:
            lines.pop(0)
        while lines and not lines[-1]:
            lines.pop()
        
        # Rejoin
        text = '\n'.join(lines)
        
        # Final trim
        text = text.strip()
        
        return text
    
    def extract_sections(self, text: str) -> dict[str, str]:
        """
        Extract common contract sections.
        
        Args:
            text: Contract text
            
        Returns:
            Dictionary of section names to text
        """
        sections = {}
        
        # Common section headers
        section_patterns = [
            r'(?:^|\n)((?:SECTION|ARTICLE|CLAUSE)\s+\d+[:\.]?\s+.+?)(?=\n(?:SECTION|ARTICLE|CLAUSE)\s+\d+|$)',
            r'(?:^|\n)(\d+\.\s+[A-Z][^.\n]{3,50}[:\.]?)(?=\n|$)',
        ]
        
        # Try to split by sections
        for pattern in section_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            for match in matches:
                section_title = match.group(1).strip()
                sections[section_title] = match.group(0).strip()
        
        return sections if sections else {'full_text': text}
    
    def split_into_clauses(self, text: str, max_length: int = 500) -> list[str]:
        """
        Split text into clause-sized chunks.
        
        Args:
            text: Contract text
            max_length: Maximum clause length in characters
            
        Returns:
            List of clause texts
        """
        clauses = []
        
        # Split by double newlines (paragraph breaks)
        paragraphs = text.split('\n\n')
        
        current_clause = []
        current_length = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            para_length = len(para)
            
            # If adding this paragraph exceeds max_length, save current clause
            if current_length + para_length > max_length and current_clause:
                clauses.append('\n\n'.join(current_clause))
                current_clause = [para]
                current_length = para_length
            else:
                current_clause.append(para)
                current_length += para_length
        
        # Add remaining clause
        if current_clause:
            clauses.append('\n\n'.join(current_clause))
        
        return clauses
