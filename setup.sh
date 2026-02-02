#!/bin/bash

# Create Streamlit config directory
mkdir -p ~/.streamlit/

# Create config file
echo "\
[general]\n\
email = \"\"\n\
\n\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = \$PORT\n\
\n\
[theme]\n\
primaryColor = \"#1f77b4\"\n\
backgroundColor = \"#ffffff\"\n\
secondaryBackgroundColor = \"#f0f2f6\"\n\
textColor = \"#262730\"\n\
font = \"sans serif\"\n\
" > ~/.streamlit/config.toml

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
