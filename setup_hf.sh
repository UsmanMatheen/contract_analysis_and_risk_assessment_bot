#!/bin/bash

# Setup script for Hugging Face Spaces deployment
# This ensures all dependencies are properly installed

echo "Installing spaCy language model..."
python -m spacy download en_core_web_lg

echo "Setup complete!"
