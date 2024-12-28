# Intelligent Cover Letter Generator

This application helps generate personalized cover letters by analyzing your resume, job descriptions, and additional materials using AI.

## Features

- Resume parsing and analysis
- Job description processing
- Company research integration
- Portfolio analysis (GitHub, Behance)
- Customizable tone and style
- PDF and text export options

## Prerequisites

- Python 3.12 or higher
- Virtual environment tool (venv recommended)
- Ollama installed and running locally (see [Ollama Installation](#ollama-setup))

### Ollama Setup

1. Install Ollama:
   ```bash
   # macOS or Linux
   curl https://ollama.ai/install.sh | sh

   # Windows
   # Download from https://ollama.ai/download/windows
   ```

2. Start Ollama:
   ```bash
   ollama serve
   ```

3. Pull the required model:
   ```bash
   ollama pull llama3.2:latest
   ```

Note: Ollama must be running (`ollama serve`) before starting the application.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cover-letter-generator.git
cd cover-letter-generator
```

2. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv cover_letter_env

# Activate virtual environment
# On Windows:
cover_letter_env\Scripts\activate
# On macOS/Linux:
source cover_letter_env/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

**Important**: The application must be run using Python's module system to ensure proper environment usage:

```bash
python -m streamlit run app.py
```

Do not run simply with `streamlit run app.py` as this may use the wrong Python environment.

The application will be available at:
- Local URL: http://localhost:8501
- Network URL: http://192.168.x.x:8501 (for accessing from other devices on your network)

## Usage

1. Upload your resume (PDF format)
2. Paste the job description
3. Enter the company name
4. (Optional) Add portfolio links or additional documents
5. Select your preferred tone and style
6. Click "Generate Cover Letter"
7. Review and download the generated cover letter in PDF or text format

## Project Structure

```
cover-letter-generator/
├── app.py                  # Main Streamlit application
├── utils/
│   ├── __init__.py
│   ├── document_processor.py
│   ├── llm_utils.py
│   ├── portfolio_agent.py
│   ├── prompt_templates.py
│   └── research_agent.py
├── requirements.txt
└── README.md
```

## Troubleshooting

If you encounter a `ModuleNotFoundError`, ensure you:
1. Have activated your virtual environment
2. Installed all requirements using `pip install -r requirements.txt`
3. Are running the application using `python -m streamlit run app.py`

## Contributing
Contributions welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
