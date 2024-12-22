import pdfminer.high_level
from typing import Dict, List
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file."""
        try:
            text = pdfminer.high_level.extract_text(pdf_path)
            return self._clean_text(text)
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    def process_job_description(self, job_description: str) -> Dict:
        """Process and structure job description text."""
        cleaned_text = self._clean_text(job_description)
        
        # Split into sections
        sections = self._split_into_sections(cleaned_text)
        
        # Extract key information
        processed = {
            'requirements': self._extract_requirements(cleaned_text),
            'responsibilities': self._extract_responsibilities(cleaned_text),
            'skills': self._extract_skills(cleaned_text),
            'full_text': cleaned_text,
            'sections': sections
        }
        
        return processed

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters
        text = re.sub(r'[^\w\s.,;:-]', '', text)
        return text.strip()

    def _split_into_sections(self, text: str) -> List[str]:
        """Split text into logical sections."""
        chunks = self.text_splitter.split_text(text)
        return chunks

    def _extract_requirements(self, text: str) -> List[str]:
        """Extract job requirements from text."""
        requirements = []
        # Look for requirement patterns
        patterns = [
            r'requirements?:?\s*(.*?)(?=\n\n|\Z)',
            r'qualifications?:?\s*(.*?)(?=\n\n|\Z)',
            r'what you\'ll need:?\s*(.*?)(?=\n\n|\Z)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            requirements.extend(matches)
        
        return list(set(requirements))

    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract job responsibilities from text."""
        responsibilities = []
        patterns = [
            r'responsibilities?:?\s*(.*?)(?=\n\n|\Z)',
            r'duties:?\s*(.*?)(?=\n\n|\Z)',
            r'what you\'ll do:?\s*(.*?)(?=\n\n|\Z)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            responsibilities.extend(matches)
        
        return list(set(responsibilities))

    def _extract_skills(self, text: str) -> List[str]:
        """Extract required skills from text."""
        skills = []
        patterns = [
            r'skills?:?\s*(.*?)(?=\n\n|\Z)',
            r'technical requirements?:?\s*(.*?)(?=\n\n|\Z)',
            r'proficienc(?:y|ies):?\s*(.*?)(?=\n\n|\Z)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            skills.extend(matches)
        
        return list(set(skills))