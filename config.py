import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application settings
APP_SETTINGS = {
    'debug': os.getenv('DEBUG', 'False') == 'True',
    'ollama_host': os.getenv('OLLAMA_HOST', 'http://localhost:11434'),
    'model_name': os.getenv('MODEL_NAME', 'llama2:13b'),
    'max_tokens': int(os.getenv('MAX_TOKENS', '2048')),
    'temperature': float(os.getenv('TEMPERATURE', '0.7')),
}

# Document processing settings
DOC_SETTINGS = {
    'max_file_size': 5 * 1024 * 1024,  # 5MB
    'allowed_file_types': ['pdf', 'docx', 'txt'],
    'chunk_size': 1000,
    'chunk_overlap': 200,
}

# Quality assurance settings
QA_SETTINGS = {
    'min_readability_score': 45,
    'max_readability_score': 70,
    'min_letter_length': 250,
    'max_letter_length': 400,
}

# Streamlit page configuration
STREAMLIT_SETTINGS = {
    'page_title': 'AI Cover Letter Generator',
    'page_icon': '📝',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
}