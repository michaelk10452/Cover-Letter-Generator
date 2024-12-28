import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Path settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, 'cache')

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

# Company research settings
RESEARCH_SETTINGS = {
    'news_api_key': os.getenv('NEWS_API_KEY', ''),
    'cache_expiration': 24 * 60 * 60,  # 24 hours in seconds
    'cache_dir': CACHE_DIR,  # Now using the CACHE_DIR constant
    'max_news_results': 3,
    'enable_web_scraping': True,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}