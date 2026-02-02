# Setup Instructions

## Initial Setup

Follow these steps to set up your development environment:

### 1. Prerequisites Check
- Python 3.9+ installed
- Git installed
- OpenAI or Anthropic API key ready

### 2. Environment Setup

```bash
# Navigate to project directory
cd contract_analysis_and_risk_assessment_bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Download NLP Models

```bash
# Download spaCy English model (large)
python -m spacy download en_core_web_lg

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your API keys
# Windows: notepad .env
# Linux/Mac: nano .env
```

Required environment variables:
```
LLM_PROVIDER=openai  # or anthropic
OPENAI_API_KEY=your_actual_api_key_here
# OR
ANTHROPIC_API_KEY=your_actual_api_key_here
```

### 5. Verify Installation

```bash
# Test imports
python -c "import streamlit; import spacy; import openai; print('All imports successful!')"
```

### 6. Run the Application

```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## Development Setup

### Git Configuration

```bash
# Initialize git (if not already done)
git init

# Add remote (if applicable)
git remote add origin <your-repo-url>

# Create .env file (never commit this)
echo ".env" >> .gitignore
```

### IDE Setup (VSCode Recommended)

Install recommended extensions:
- Python
- Pylance
- Python Docstring Generator
- GitLens

### Testing Setup

```bash
# Install testing dependencies
pip install pytest pytest-cov pytest-asyncio

# Run tests
pytest tests/
```

## Troubleshooting

### Issue: spaCy model not found
```bash
python -m spacy download en_core_web_lg --force
```

### Issue: NLTK data not found
```python
import nltk
nltk.download('all')
```

### Issue: API key errors
- Verify API key is correctly set in .env
- Check that .env file is in project root
- Restart the Streamlit application

### Issue: Import errors
```bash
pip install --upgrade -r requirements.txt
```

## Next Steps

After successful setup, proceed to implement the core modules:
1. Document Parser (Phase 2)
2. NLP Processor (Phase 3)
3. LLM Handler (Phase 4)
4. And so on...

## Production Deployment

See `docs/DEPLOYMENT.md` for production deployment instructions.
