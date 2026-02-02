"""Example usage of document parser."""

from pathlib import Path
from src.document_parser import DocumentParser
from src.utils import setup_logging

# Initialize logging
logger = setup_logging()


def parse_sample_document():
    """Example of parsing a document."""
    
    print("\n" + "="*60)
    print("Document Parser - Example Usage")
    print("="*60 + "\n")
    
    # Initialize parser
    parser = DocumentParser()
    
    # Example 1: Parse from sample text (simulating uploaded file)
    sample_text = """
    EMPLOYMENT AGREEMENT
    
    This Employment Agreement ("Agreement") is entered into on January 1, 2026,
    between ABC Technologies Private Limited ("Employer") and John Doe ("Employee").
    
    1. POSITION AND DUTIES
    The Employee shall serve as Software Engineer and shall perform duties as assigned.
    
    2. COMPENSATION
    The Employee shall receive a salary of INR 10,00,000 per annum, payable monthly.
    
    3. TERM
    This Agreement shall commence on January 1, 2026 and continue until terminated
    by either party with 30 days written notice.
    
    4. CONFIDENTIALITY
    The Employee agrees to maintain confidentiality of all proprietary information.
    
    5. NON-COMPETE
    The Employee agrees not to engage in competing business for 12 months after
    termination within a 50 km radius.
    """
    
    # Parse the text
    result = parser.parse(
        file_bytes=sample_text.encode('utf-8'),
        filename="sample_employment_contract.txt"
    )
    
    # Display results
    print(f"📄 File: {result.metadata['filename']}")
    print(f"📝 Type: {result.file_type.upper()}")
    print(f"🌐 Language: {result.language}")
    print(f"📊 Word Count: {result.word_count}")
    print(f"📏 Character Count: {result.char_count}")
    print(f"✓ Valid: {result.is_valid}")
    
    if result.is_valid:
        print("\n" + "-"*60)
        print("Extracted Text (Preview):")
        print("-"*60)
        print(result.text[:500] + "..." if len(result.text) > 500 else result.text)
        
        # Split into clauses
        from src.document_parser.text_cleaner import TextCleaner
        cleaner = TextCleaner()
        clauses = cleaner.split_into_clauses(result.text, max_length=300)
        
        print("\n" + "-"*60)
        print(f"Clause Breakdown ({len(clauses)} clauses):")
        print("-"*60)
        for i, clause in enumerate(clauses, 1):
            print(f"\nClause {i} ({len(clause)} chars):")
            preview = clause[:150].replace('\n', ' ')
            print(f"  {preview}...")
    else:
        print(f"\n❌ Error: {result.error_message}")
    
    print("\n" + "="*60)
    print("Example Complete")
    print("="*60 + "\n")


if __name__ == "__main__":
    parse_sample_document()
