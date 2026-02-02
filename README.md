# 📜 Contract Analysis & Risk Assessment Bot

A sophisticated GenAI-powered legal assistant that helps small and medium business owners understand complex contracts, identify potential legal risks, and receive actionable advice in plain language.

## 🎯 Features

### Core Capabilities
- **Contract Type Classification**: Automatically identifies employment agreements, vendor contracts, lease agreements, partnership deeds, and service contracts
- **Intelligent Analysis**: Clause-by-clause extraction and explanation in simple business language
- **Risk Assessment**: Comprehensive risk scoring at both clause and contract levels
- **Multilingual Support**: Processes contracts in English and Hindi
- **Actionable Insights**: Identifies unfavorable terms and suggests alternatives
- **Compliance Checking**: Validates against common Indian legal standards
- **Template Library**: Access to SME-friendly standardized contract templates

### Risk Detection
- Penalty & Indemnity Clauses
- Unilateral Termination Terms
- Arbitration & Jurisdiction Issues
- Auto-Renewal & Lock-in Periods
- Non-compete & IP Transfer Clauses
- Ambiguous or Unclear Language

### Output Formats
- Plain-language contract summaries
- Clause-by-clause explanations
- Risk mitigation strategies
- Professional PDF reports for legal review
- Complete audit trails for compliance

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- OpenAI API key (GPT-4) or Anthropic API key (Claude 3)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd contract_analysis_and_risk_assessment_bot
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download spaCy models**
```bash
python -m spacy download en_core_web_lg
```

5. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

6. **Run the application**
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage

1. **Upload Contract**: Upload PDF, DOCX, or TXT files (up to 10MB)
2. **Select Language**: Choose English or Hindi
3. **Analyze**: Click "Analyze Contract" to process
4. **Review Results**: 
   - View contract classification and summary
   - Review clause-by-clause analysis
   - Check risk assessment scores
   - Examine flagged unfavorable terms
5. **Export**: Download PDF report for legal consultation
6. **Templates**: Browse and download SME-friendly contract templates

## 🛠️ Technology Stack

- **LLM**: GPT-4 (OpenAI) or Claude 3 (Anthropic)
- **NLP**: spaCy, NLTK
- **UI**: Streamlit
- **Document Processing**: PyPDF2, python-docx, pdfplumber
- **Report Generation**: ReportLab, WeasyPrint
- **Data Storage**: JSON-based audit logs

## 📂 Project Structure

```
contract_analysis_bot/
├── app.py                    # Main Streamlit application
├── config/                   # Configuration files
├── src/                      # Source code modules
│   ├── document_parser/      # Document processing
│   ├── nlp_processor/        # NLP pipelines
│   ├── llm_handler/          # LLM integration
│   ├── contract_analyzer/    # Contract analysis
│   ├── risk_engine/          # Risk assessment
│   ├── template_manager/     # Template management
│   └── report_generator/     # Report generation
├── data/                     # Data storage
│   ├── templates/            # Contract templates
│   ├── audit_logs/           # Audit trails
│   └── uploads/              # Temporary storage
├── ui/                       # UI components
└── docs/                     # Documentation
```

## 🔒 Security & Privacy

- All uploaded contracts are processed locally
- No data is stored on external servers
- Complete audit trails for compliance
- API keys stored securely in environment variables
- Automatic cleanup of temporary files

## 📊 Risk Scoring

- **Low Risk (0-30%)**: Standard contract terms
- **Medium Risk (30-60%)**: Terms requiring attention
- **High Risk (60-80%)**: Potentially unfavorable terms
- **Critical Risk (80-100%)**: Terms requiring immediate review

## 🌐 Supported Contract Types

1. Employment Agreements
2. Vendor Contracts
3. Lease Agreements
4. Partnership Deeds
5. Service Contracts
6. Non-Disclosure Agreements (NDAs)
7. Consultancy Agreements
8. Purchase Orders

## 📝 License

This project is proprietary software developed for SME contract analysis.

## 🤝 Support

For issues, questions, or feature requests, please contact the development team.

## 🔄 Version History

- **v1.0.0** (2026-02-02): Initial release with core features

---

**Built for Indian SMEs | Powered by GenAI | Secure & Confidential**
