# AI Cover Letter Generator

A sophisticated application that generates tailored cover letters by analyzing your professional documents and online presence. Built with Python and modern AI technologies, it creates personalized cover letters that authentically represent your experience and qualifications.

## Features

### Document Processing
- PDF resume parsing and analysis
- Multiple document support (transcripts, certifications)
- Automatic skill and experience extraction
- Structured job description analysis

### Portfolio Integration
- GitHub repository analysis
  - Project detection and analysis
  - Language identification
  - Repository statistics
- Behance portfolio integration
- Support for additional portfolio platforms

### Company Research
- Automatic company name detection
- Manual company name override
- Verified company information integration
- Industry and focus area analysis

### Customization
- Multiple tone options (Professional, Enthusiastic, Confident, Conservative)
- Writing style selection (Standard, Creative, Technical, Executive)
- Format customization
- Export options (PDF, Text)

## Installation

### Prerequisites
- Python 3.12 or higher
- Ollama (for local LLM deployment)

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/cover-letter-generator.git
cd cover-letter-generator

# Create and activate virtual environment
python -m venv cover_letter_env
source cover_letter_env/bin/activate  # On Windows: cover_letter_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Ollama (if not already installed)
# For Linux/WSL:
curl https://ollama.ai/install.sh | sh
# For MacOS:
brew install ollama

# Pull the required model
ollama pull llama3.2:latest
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Upload Documents:
   - Primary resume (PDF)
   - Additional supporting documents
   - Portfolio links (GitHub, Behance)

3. Enter Job Information:
   - Paste job description
   - Enter/verify company name
   - Select research preferences

4. Customize Output:
   - Choose tone and style
   - Select information to include
   - Review portfolio analysis

5. Generate and Export:
   - Review generated cover letter
   - Export as PDF or text
   - Check sourced information

## Technical Architecture
```
cover_letter_generator/
├── app.py                  # Main application
├── utils/
│   ├── document_processor.py  # Document handling
│   ├── llm_utils.py          # LLM integration
│   ├── portfolio_agent.py    # Portfolio analysis
│   ├── research_agent.py     # Company research
│   └── prompt_templates.py   # Prompt engineering
├── templates/              # Letter templates
└── tests/                 # Test suite
```

## Technology Stack
- **Core**: Python, Streamlit
- **AI/ML**: Ollama, LangChain
- **Document Processing**: PyPDF, PDFMiner
- **Web Integration**: BeautifulSoup4, Requests
- **Data Analysis**: NLTK, spaCy
- **Export**: ReportLab

## Contributing
Contributions welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.