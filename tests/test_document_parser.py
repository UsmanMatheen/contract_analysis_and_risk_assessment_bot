"""Tests for document parser module."""

import os
from pathlib import Path
from src.document_parser import DocumentParser


def test_document_parser():
    """Quick test of document parser functionality."""
    parser = DocumentParser()
    
    print("=" * 60)
    print("Document Parser Test Suite")
    print("=" * 60)
    
    # Test 1: Check supported formats
    print("\n1. Supported Formats:")
    formats = parser.get_supported_formats()
    print(f"   {', '.join(formats)}")
    
    # Test 2: File size validation
    print("\n2. File Size Validation:")
    test_sizes = [
        (1024 * 1024, "1 MB"),
        (5 * 1024 * 1024, "5 MB"),
        (15 * 1024 * 1024, "15 MB")
    ]
    
    for size, label in test_sizes:
        is_valid = parser.validate_file_size(size)
        status = "✓ Valid" if is_valid else "✗ Too large"
        print(f"   {label}: {status}")
    
    # Test 3: Text cleaning
    print("\n3. Text Cleaning Test:")
    from src.document_parser.text_cleaner import TextCleaner
    cleaner = TextCleaner()
    
    test_text = """
    This is a    test   document.
    
    
    Page 1
    
    It has    multiple   spaces and    newlines.
    
    
    
    This should be    cleaned.
    """
    
    cleaned = cleaner.clean(test_text)
    print(f"   Original length: {len(test_text)} chars")
    print(f"   Cleaned length: {len(cleaned)} chars")
    print(f"   Preview: {cleaned[:100]}...")
    
    # Test 4: Clause splitting
    print("\n4. Clause Splitting Test:")
    sample_contract = """
    SECTION 1: DEFINITIONS
    
    This Agreement defines the terms between parties.
    
    SECTION 2: OBLIGATIONS
    
    Party A shall deliver the goods within 30 days.
    Party B shall make payment upon delivery.
    
    SECTION 3: TERMINATION
    
    Either party may terminate with 30 days notice.
    """
    
    clauses = cleaner.split_into_clauses(sample_contract, max_length=200)
    print(f"   Split into {len(clauses)} clauses")
    for i, clause in enumerate(clauses, 1):
        print(f"   Clause {i}: {len(clause)} chars")
    
    print("\n" + "=" * 60)
    print("Document Parser Tests Complete ✓")
    print("=" * 60)


if __name__ == "__main__":
    test_document_parser()
