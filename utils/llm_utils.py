import requests
from typing import Dict, List
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
import datetime
import re
from config import APP_SETTINGS

class OllamaLLM:
    def __init__(self):
        self.model_name = APP_SETTINGS['model_name']
        self.host = APP_SETTINGS['ollama_host']
        self.temperature = APP_SETTINGS['temperature']
        self.max_tokens = APP_SETTINGS['max_tokens']
        self._verify_model_availability()

    def _verify_model_availability(self):
        try:
            response = requests.get(f"{self.host}/api/tags")
            if response.status_code == 200:
                available_models = response.json()
                if not any(model['name'] == self.model_name for model in available_models['models']):
                    raise Exception(f"Model {self.model_name} not found. Please pull it using 'ollama pull {self.model_name}'")
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to Ollama server. Please ensure it's running.")

    def generate_cover_letter(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.temperature,
                        "top_p": 0.9,
                        "top_k": 40,
                        "num_ctx": 4096,
                        "stop": ["[END]"]
                    }
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result['response'].strip()
                
                # Format the cover letter with proper structure
                formatted_letter = self._format_cover_letter(generated_text)
                return formatted_letter
            else:
                raise Exception(f"Error generating cover letter: {response.text}")
                
        except Exception as e:
            raise Exception(f"Error communicating with Ollama: {str(e)}")

    def _format_cover_letter(self, text: str) -> str:
        """Format the cover letter with proper business letter structure."""
        # Clean up the text
        text = re.sub(r'Here is.*?:\n', '', text)
        text = re.sub(r'\[.*?\]', '', text)
        text = re.sub(r'About the position:?\n?', '', text)
        text = re.sub(r'Contact Information:?\n?', '', text)
        
        # Split into paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # Get current date
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        
        # Format the letter
        formatted_parts = [
            current_date + "\n",  # Add newline after date
            "Dear Hiring Manager,\n"  # Single greeting
        ]
        
        # Add body paragraphs (exclude anything that looks like a header or signature)
        for p in paragraphs:
            if not any(x in p.lower() for x in [
                'dear hiring manager', 
                'sincerely', 
                'recruiting team', 
                'contact information',
                'phone:',
                'email:',
                '@gmail.com'
            ]):
                formatted_parts.append("\n" + p)
        
        # Add signature
        formatted_parts.extend([
            "\n\nSincerely,",
            "\n[Your Name]",
            "[Your Email]",
            "[Your Phone]"
        ])
        
        return "\n".join(formatted_parts)

    def export_to_pdf(self, cover_letter_text: str, filename: str = "cover_letter.pdf") -> BytesIO:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
        styles = getSampleStyleSheet()
        
        # Create custom styles
        header_style = ParagraphStyle(
            'Header',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=30
        )
        
        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontSize=12,
            leading=14,
            spaceBefore=12,
            spaceAfter=12
        )
        
        signature_style = ParagraphStyle(
            'Signature',
            parent=styles['Normal'],
            fontSize=12,
            spaceBefore=30
        )
        
        # Split the letter into sections
        sections = cover_letter_text.split('\n\n')
        story = []
        
        # Add each section with appropriate styling
        for i, section in enumerate(sections):
            if i == 0:  # Date
                story.append(Paragraph(section, header_style))
            elif i == len(sections) - 1:  # Signature
                story.append(Paragraph(section, signature_style))
            else:
                story.append(Paragraph(section, body_style))
        
        # Build the PDF
        doc.build(story)
        buffer.seek(0)
        return buffer

    def get_model_info(self) -> Dict:
        try:
            response = requests.get(f"{self.host}/api/show", params={"name": self.model_name})
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error getting model info: {response.text}")
        except Exception as e:
            raise Exception(f"Error communicating with Ollama: {str(e)}")

    def generate_with_history(self, prompt: str, history: List[Dict] = None) -> str:
        if history is None:
            history = []
            
        try:
            response = requests.post(
                f"{self.host}/api/chat",
                json={
                    "model": self.model_name,
                    "messages": history + [{"role": "user", "content": prompt}],
                    "stream": False,
                    "options": {
                        "temperature": self.temperature,
                        "top_p": 0.9
                    }
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['message']['content'].strip()
            else:
                raise Exception(f"Error generating response: {response.text}")
                
        except Exception as e:
            raise Exception(f"Error communicating with Ollama: {str(e)}")