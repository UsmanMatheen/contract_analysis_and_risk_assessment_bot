---
title: Contract Analysis & Risk Assessment
emoji: ⚖️
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.31.0
app_file: app.py
pinned: false
license: mit
tags:
  - contract-analysis
  - legal-tech
  - nlp
  - risk-assessment
  - genai
  - gpt-4
  - claude
  - streamlit
---

# ⚖️ Contract Analysis & Risk Assessment Platform

An enterprise-grade GenAI-powered legal assistant that helps small and medium business owners understand complex contracts, identify potential legal risks, and receive actionable advice in plain language.

## 🎯 Features

### Core Capabilities
- **AI-Powered Contract Classification**: Automatically identifies contract types (employment, vendor, lease, partnership, service agreements)
- **Intelligent Clause Analysis**: Deep clause-by-clause extraction and plain-language explanations
- **Comprehensive Risk Assessment**: Multi-level risk scoring with severity categorization
- **Multilingual Support**: Processes contracts in English and Hindi
- **Smart Entity Recognition**: Extracts parties, dates, amounts, obligations, and key terms
- **Template Library**: Access standardized SME-friendly contract templates
- **Professional Reports**: Generate detailed PDF analysis reports

### Risk Detection Engine
- ✓ Penalty & Indemnity Clauses
- ✓ Unilateral Termination Terms
- ✓ Arbitration & Jurisdiction Issues
- ✓ Auto-Renewal & Lock-in Periods
- ✓ Non-compete & IP Transfer Clauses
- ✓ Liability & Warranty Terms
- ✓ Ambiguous Language Detection

### Technology Stack
- **LLM**: GPT-4 / Claude 3 for legal reasoning
- **NLP**: spaCy + NLTK for preprocessing and entity extraction
- **Document Processing**: Multi-format support (PDF, DOCX, TXT)
- **UI**: Professional Streamlit interface
- **Reports**: ReportLab for PDF generation

## 🚀 How to Use

1. **Upload Contract**: Upload your contract in PDF, DOCX, or TXT format
2. **Configure Analysis**: Select document language and analysis depth
3. **Analyze**: Click "Begin Analysis" to start AI-powered processing
4. **Review Results**: Get comprehensive analysis including:
   - Contract type and summary
   - Clause-by-clause breakdown
   - Risk assessment with severity levels
   - Key entities and obligations
   - Actionable recommendations
5. **Export Report**: Download professional PDF reports for legal review

## 📋 Supported Contract Types

- Employment Agreements
- Vendor Contracts
- Lease Agreements
- Partnership Deeds
- Service Contracts
- Non-Disclosure Agreements (NDAs)
- Consultancy Agreements
- Purchase Orders

## 🔐 Privacy & Security

- All analysis is performed securely
- No contract data is stored permanently
- Complete audit trails maintained
- API keys encrypted and secured

## ⚠️ Disclaimer

This tool provides AI-generated analysis for **informational purposes only**. It is not a substitute for professional legal advice. Always consult with qualified legal counsel before making decisions based on this analysis.

## 📚 About

Built as an enterprise-grade solution for small and medium businesses to:
- Understand complex legal agreements
- Identify potential risks and liabilities
- Make informed business decisions
- Reduce dependency on expensive legal consultations

**Developer**: Professional GenAI Application  
**License**: MIT  
**Repository**: [GitHub](https://github.com/UsmanMatheen/contract_analysis_and_risk_assessment_bot)

---

### Configuration Required

To use this app, you need to configure your API key in the Space settings:

1. Go to **Settings** → **Repository secrets**
2. Add your `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
3. Restart the Space

For detailed configuration options, see `.streamlit/secrets.toml.example` in the repository.
