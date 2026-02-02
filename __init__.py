"""
Contract Analysis and Risk Assessment Bot
==========================================

A sophisticated GenAI-powered legal assistant for small and medium business owners.

Author: Contract Analysis Team
Version: 1.0.0
License: Proprietary

For documentation, see:
- README.md - Project overview and quick start
- docs/USER_GUIDE.md - Complete user documentation
- docs/API.md - API documentation for developers
- docs/DEPLOYMENT.md - Production deployment guide

Quick Start:
-----------
1. Install dependencies:
   pip install -r requirements.txt
   python -m spacy download en_core_web_lg

2. Configure environment:
   cp .env.example .env
   # Edit .env and add your API key

3. Run the application:
   streamlit run app.py

4. Open browser:
   http://localhost:8501

Modules:
--------
- document_parser: Parse PDF/DOCX/TXT files
- nlp_processor: Extract clauses and entities
- llm_handler: GPT-4/Claude integration
- contract_analyzer: Main analysis orchestration
- risk_engine: Risk assessment and scoring
- template_manager: Contract templates
- report_generator: PDF report generation

For Support:
-----------
Contact your system administrator or refer to the documentation.
"""

__version__ = "1.0.0"
__author__ = "Contract Analysis Team"
__license__ = "Proprietary"

# Package information
__all__ = [
    'contract_analyzer',
    'document_parser',
    'llm_handler',
    'nlp_processor',
    'report_generator',
    'risk_engine',
    'template_manager',
    'audit',
    'utils'
]
