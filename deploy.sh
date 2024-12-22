#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install it first."
    exit 1
fi

# Check if virtualenv is installed
if ! command -v virtualenv &> /dev/null; then
    echo "Installing virtualenv..."
    pip install virtualenv
fi

# Create and activate virtual environment
python3 -m venv cover_letter_env
source cover_letter_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install spaCy model
python -m spacy download en_core_web_sm

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl https://ollama.ai/install.sh | sh
fi

# Pull the required model
ollama pull llama2:13b

# Create necessary directories if they don't exist
mkdir -p templates
mkdir -p utils
mkdir -p data
mkdir -p models
mkdir -p tests

# Run tests
python -m pytest tests/

# Start the application
echo "Starting the application..."
ollama serve &
streamlit run app.py