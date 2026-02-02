"""Quick start script to verify installation."""

import sys
from pathlib import Path

def check_imports():
    """Check if all required packages are installed."""
    
    print("\n" + "="*60)
    print("Checking Installation")
    print("="*60 + "\n")
    
    packages = {
        'streamlit': 'Streamlit',
        'spacy': 'spaCy',
        'nltk': 'NLTK',
        'openai': 'OpenAI',
        'anthropic': 'Anthropic',
        'PyPDF2': 'PyPDF2',
        'pdfplumber': 'pdfplumber',
        'docx': 'python-docx',
        'langdetect': 'langdetect',
        'reportlab': 'ReportLab',
        'loguru': 'Loguru',
        'pydantic': 'Pydantic'
    }
    
    missing = []
    
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"✓ {name}")
        except ImportError:
            print(f"✗ {name} - NOT FOUND")
            missing.append(name)
    
    if missing:
        print(f"\n✗ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✓ All packages installed\n")
    return True


def check_spacy_model():
    """Check if spaCy model is downloaded."""
    
    print("Checking spaCy model...")
    
    try:
        import spacy
        nlp = spacy.load("en_core_web_lg")
        print("✓ spaCy model (en_core_web_lg) is installed\n")
        return True
    except OSError:
        print("✗ spaCy model not found")
        print("Run: python -m spacy download en_core_web_lg\n")
        return False


def check_env_file():
    """Check if .env file exists."""
    
    print("Checking environment configuration...")
    
    env_file = Path(".env")
    if env_file.exists():
        print("✓ .env file exists")
        
        # Check for API key
        content = env_file.read_text()
        if 'OPENAI_API_KEY' in content or 'ANTHROPIC_API_KEY' in content:
            if 'your_' not in content.lower() and 'change' not in content.lower():
                print("✓ API key appears to be configured\n")
                return True
            else:
                print("⚠ API key needs to be set in .env file\n")
                return False
        else:
            print("⚠ API key not found in .env file\n")
            return False
    else:
        print("✗ .env file not found")
        print("Run: cp .env.example .env")
        print("Then edit .env and add your API key\n")
        return False


def check_directories():
    """Check if required directories exist."""
    
    print("Checking directory structure...")
    
    dirs = ['data', 'data/templates', 'data/audit_logs', 'data/uploads', 'logs']
    all_exist = True
    
    for dir_name in dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✓ {dir_name}/")
        else:
            print(f"✗ {dir_name}/ - creating...")
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ Created")
    
    print()
    return True


def run_quick_test():
    """Run a quick functionality test."""
    
    print("Running quick functionality test...")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        
        from config.settings import get_settings
        from src.document_parser import DocumentParser
        from src.nlp_processor import NLPProcessor
        
        # Test settings
        settings = get_settings()
        print(f"✓ Settings loaded: {settings.APP_NAME}")
        
        # Test document parser
        parser = DocumentParser()
        print("✓ Document parser initialized")
        
        # Test NLP processor
        nlp = NLPProcessor()
        print("✓ NLP processor initialized")
        
        # Test basic parsing
        sample_text = "This is a test contract. The parties agree to the terms."
        result = parser.parse(
            file_bytes=sample_text.encode('utf-8'),
            filename="test.txt"
        )
        
        if result.is_valid:
            print(f"✓ Document parsing works (detected {result.word_count} words)")
        else:
            print(f"✗ Document parsing failed: {result.error_message}")
            return False
        
        # Test NLP
        nlp_result = nlp.process(sample_text)
        if nlp_result:
            print(f"✓ NLP processing works (found {nlp_result['statistics']['total_clauses']} clauses)")
        
        print()
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main verification script."""
    
    print("\n" + "="*60)
    print("Contract Analysis Bot - Installation Verification")
    print("="*60)
    
    checks = [
        ("Package Installation", check_imports),
        ("spaCy Model", check_spacy_model),
        ("Environment Configuration", check_env_file),
        ("Directory Structure", check_directories),
        ("Functionality Test", run_quick_test)
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ {name} check failed: {str(e)}\n")
            results.append((name, False))
    
    # Summary
    print("="*60)
    print("Summary")
    print("="*60 + "\n")
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(r[1] for r in results)
    
    print()
    print("="*60)
    
    if all_passed:
        print("✓ All checks passed! You're ready to run the application.")
        print("\nTo start the application, run:")
        print("  streamlit run app.py")
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  1. Install packages: pip install -r requirements.txt")
        print("  2. Download spaCy model: python -m spacy download en_core_web_lg")
        print("  3. Setup .env: cp .env.example .env (then edit with your API key)")
    
    print("="*60 + "\n")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
