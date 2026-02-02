# API Documentation

## Overview

The Contract Analysis Bot provides a programmatic API for integration into other applications.

## Core Modules

### 1. Document Parser

```python
from src.document_parser import DocumentParser

# Initialize
parser = DocumentParser()

# Parse from file
result = parser.parse(file_path="contract.pdf")

# Parse from bytes
with open("contract.pdf", "rb") as f:
    result = parser.parse(file_bytes=f.read(), filename="contract.pdf")

# Check result
if result.is_valid:
    print(f"Text: {result.text}")
    print(f"Language: {result.language}")
    print(f"Word count: {result.word_count}")
else:
    print(f"Error: {result.error_message}")
```

**ParsedDocument Attributes:**
- `text`: Extracted text
- `metadata`: Document metadata (title, author, etc.)
- `language`: Detected language ('en' or 'hi')
- `file_type`: File extension
- `page_count`: Number of pages (PDF only)
- `word_count`: Total words
- `is_valid`: Whether parsing succeeded
- `error_message`: Error if parsing failed

### 2. NLP Processor

```python
from src.nlp_processor import NLPProcessor

# Initialize
nlp = NLPProcessor()

# Process text
results = nlp.process(contract_text)

# Access results
clauses = results['clauses']
entities = results['entities']
key_terms = results['key_terms']
statistics = results['statistics']
```

**Clause Object:**
- `id`: Unique identifier
- `text`: Clause text
- `clause_type`: 'obligation', 'right', 'prohibition', or 'general'
- `section_number`: Section reference
- `keywords`: Risk-related keywords
- `entities`: Extracted entities
- `sentence_count`: Number of sentences
- `word_count`: Number of words

### 3. LLM Handler

```python
from src.llm_handler import LLMHandler

# Initialize
llm = LLMHandler()

# Classify contract
classification = llm.classify_contract(contract_text)
print(f"Type: {classification['contract_type']}")

# Analyze clause
analysis = llm.analyze_clause(clause_text)
print(analysis['plain_language_explanation'])

# Assess risks
risks = llm.assess_risks(contract_text)
for risk in risks['risks']:
    print(f"{risk['category']}: {risk['level']}")

# Generate summary
summary = llm.generate_summary(contract_text)
print(summary['summary'])

# Identify unfavorable terms
unfavorable = llm.identify_unfavorable_terms(contract_text)
for term in unfavorable['unfavorable_terms']:
    print(term['description'])

# Suggest alternatives
suggestion = llm.suggest_alternative_clause(
    original_clause="Employee shall not compete...",
    issue="Overly broad non-compete"
)
print(suggestion['suggested_alternative'])
```

### 4. Contract Analyzer

```python
from src.contract_analyzer import ContractAnalyzer

# Initialize
analyzer = ContractAnalyzer()

# Full analysis
results = analyzer.analyze_contract(
    file_path="contract.pdf"
)

# Or from bytes
results = analyzer.analyze_contract(
    file_bytes=contract_bytes,
    filename="contract.pdf"
)

# Access results
if results['status'] == 'success':
    print(f"Contract Type: {results['contract_classification']['contract_type']}")
    print(f"Risk Level: {results['risk_assessment']['overall_risk_level']}")
    print(f"Clauses: {results['nlp_analysis']['total_clauses']}")
    
    # Export as JSON
    json_export = analyzer.export_analysis(results, format='json')
    
    # Export as text
    text_export = analyzer.export_analysis(results, format='text')
```

### 5. Risk Engine

```python
from src.risk_engine import RiskEngine

# Initialize
engine = RiskEngine()

# Assess contract
risk_assessment = engine.assess_contract(
    contract_text=text,
    clauses=clause_list
)

# Get overall score
overall_score = risk_assessment['overall_risk_score']
risk_level = risk_assessment['overall_risk_level']

# Get identified risks
for risk in risk_assessment['identified_risks']:
    print(f"Category: {risk['category']}")
    print(f"Severity: {risk['severity']}")
    print(f"Description: {risk['description']}")
    print(f"Recommendation: {risk['recommendation']}")

# Get high-risk clauses
high_risk = risk_assessment['high_risk_clauses']
```

### 6. Template Manager

```python
from src.template_manager import TemplateManager

# Initialize
templates = TemplateManager()

# List available templates
template_list = templates.list_templates()
for template in template_list:
    print(f"{template['title']}: {template['description']}")

# Get specific template
template = templates.get_template('employment_agreement')
print(template['content'])

# Generate contract from template
contract = templates.generate_contract(
    template_name='employment_agreement',
    variables={
        'COMPANY_NAME': 'ABC Corp',
        'EMPLOYEE_NAME': 'John Doe',
        'POSITION': 'Software Engineer',
        'START_DATE': '2026-03-01',
        'SALARY': '1,200,000',
        'LOCATION': 'Mumbai',
        'NOTICE_PERIOD': '30'
    }
)
print(contract)
```

### 7. Report Generator

```python
from src.report_generator import ReportGenerator

# Initialize
generator = ReportGenerator()

# Generate full report
pdf_bytes = generator.generate_full_report(
    analysis_results=results,
    output_path='reports/full_report.pdf'  # Optional
)

# Generate summary report
summary_pdf = generator.generate_summary_report(
    analysis_results=results,
    output_path='reports/summary.pdf'
)

# Save to file
with open('contract_analysis.pdf', 'wb') as f:
    f.write(pdf_bytes)
```

### 8. Audit Logger

```python
from src.audit import AuditLogger

# Initialize
audit = AuditLogger()

# Log activity
entry_id = audit.log_activity(
    activity_type='contract_upload',
    details={'filename': 'contract.pdf', 'size': 1024000},
    session_id='session_123'
)

# Log specific events
audit.log_contract_upload('contract.pdf', 1024000, 'application/pdf', 'session_123')
audit.log_analysis_request('Employment Agreement', 'en', 'session_123')
audit.log_analysis_completion('session_123', results, 45.2)
audit.log_report_export('full', 'pdf', 'session_123')

# Get session history
history = audit.get_session_history('session_123')
for entry in history:
    print(f"{entry['timestamp']}: {entry['activity_type']}")
```

## Configuration

```python
from config.settings import get_settings

# Get settings instance
settings = get_settings()

# Access configuration
print(settings.LLM_PROVIDER)
print(settings.OPENAI_MODEL)
print(settings.MAX_UPLOAD_SIZE_MB)
print(settings.CONTRACT_TYPES)

# Validate API keys
if settings.validate_api_keys():
    print("API keys configured")

# Get risk level from score
risk_level = settings.get_risk_level(0.75)  # Returns "High"
```

## Error Handling

All modules include comprehensive error handling:

```python
try:
    results = analyzer.analyze_contract(file_path="contract.pdf")
    if results['status'] == 'error':
        print(f"Error: {results['error_message']}")
except Exception as e:
    print(f"Exception: {str(e)}")
```

## Logging

All modules use structured logging:

```python
from src.utils import setup_logging, get_logger

# Setup logging (once at application start)
setup_logging()

# Get logger
logger = get_logger()

# Use logger
logger.info("Processing contract")
logger.warning("Large file detected")
logger.error("Analysis failed", exc_info=True)
```

## Complete Example

```python
from src.contract_analyzer import ContractAnalyzer
from src.risk_engine import RiskEngine
from src.report_generator import ReportGenerator
from src.audit import AuditLogger

# Initialize
analyzer = ContractAnalyzer()
risk_engine = RiskEngine()
report_gen = ReportGenerator()
audit = AuditLogger()

session_id = "unique_session_id"

# Log upload
audit.log_contract_upload("contract.pdf", 1024000, "pdf", session_id)

# Analyze
results = analyzer.analyze_contract(file_path="contract.pdf")

if results['status'] == 'success':
    # Additional risk analysis
    clauses = results['detailed_data']['all_clauses']
    risk_analysis = risk_engine.assess_contract(
        contract_text=results['summary']['summary'],
        clauses=clauses
    )
    
    # Add to results
    results['risk_engine_analysis'] = risk_analysis
    
    # Log completion
    audit.log_analysis_completion(session_id, results, 60.5)
    
    # Generate report
    pdf_bytes = report_gen.generate_full_report(results)
    
    with open('output_report.pdf', 'wb') as f:
        f.write(pdf_bytes)
    
    # Log export
    audit.log_report_export('full', 'pdf', session_id)
    
    print("Analysis complete!")
    print(f"Risk Level: {results['risk_assessment']['overall_risk_level']}")
else:
    print(f"Analysis failed: {results['error_message']}")
    audit.log_error("AnalysisError", results['error_message'], session_id)
```

## Response Formats

### Analysis Results Structure

```json
{
  "status": "success",
  "analysis_id": "analysis_20260202_120000",
  "timestamp": "2026-02-02T12:00:00",
  "processing_time_seconds": 45.2,
  "document_info": {
    "filename": "contract.pdf",
    "file_type": "pdf",
    "language": "en",
    "word_count": 2500,
    "page_count": 10
  },
  "contract_classification": {
    "contract_type": "Employment Agreement",
    "justification": "...",
    "confidence": "high"
  },
  "summary": {
    "summary": "Plain language summary...",
    "key_sections": {}
  },
  "nlp_analysis": {
    "total_clauses": 25,
    "obligations": 10,
    "rights": 8,
    "prohibitions": 3,
    "entities": {},
    "key_terms": []
  },
  "risk_assessment": {
    "overall_risk_score": 0.65,
    "overall_risk_level": "High",
    "identified_risks": [],
    "recommendations": []
  }
}
```

## Rate Limits

Be aware of LLM API rate limits:
- OpenAI GPT-4: Check your account limits
- Anthropic Claude: Check your account limits

Implement appropriate rate limiting and error handling in production.

## Best Practices

1. **Always validate input files** before processing
2. **Implement timeout handling** for long-running analyses
3. **Cache results** when appropriate
4. **Monitor API usage** to avoid unexpected costs
5. **Handle errors gracefully** with proper error messages
6. **Use logging** for debugging and audit trails
7. **Validate API keys** before starting analysis
8. **Clean up temporary files** after processing

---

For more information, see the source code documentation and examples folder.
