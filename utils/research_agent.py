import requests
from bs4 import BeautifulSoup
from typing import Dict, List
import json
from datetime import datetime
import re
import nltk

class CompanyResearchAgent:
    def __init__(self):
        try:
            nltk.data.find('punkt')
        except LookupError:
            nltk.download('punkt')
            
        # Pre-defined research for major companies
        self.company_data = {
            "samsung research america": {
                "overview": "Samsung Research America (SRA) is the North American research arm of Samsung Electronics, focusing on advanced technology development in artificial intelligence, machine learning, security, mobile health, and other emerging areas.",
                "values": ["Innovation", "Excellence", "Change", "Integrity", "Co-prosperity"],
                "recent_news": [
                    {
                        "title": "Samsung's Commitment to AI Research and Development",
                        "summary": "Samsung continues to expand its AI research capabilities, with focus on next-generation mobile technology and user experience."
                    }
                ],
                "focus_areas": [
                    "Artificial Intelligence",
                    "Machine Learning",
                    "Mobile Technologies",
                    "Healthcare Innovation",
                    "Security Research"
                ]
            }
        }

    def research_company(self, company_name: str) -> Dict:
        """
        Research company information from multiple sources.
        """
        company_name = company_name.lower().strip()
        results = {
            'company_name': company_name,
            'overview': '',
            'recent_news': [],
            'values': [],
            'focus_areas': [],
            'error': None
        }

        try:
            # Check pre-defined data first
            if company_name in self.company_data:
                return self.company_data[company_name]

            # Fallback to dynamic research
            company_info = self._get_company_info(company_name)
            if company_info:
                results.update(company_info)

            news = self._search_company_news(company_name)
            if news:
                results['recent_news'] = news

        except Exception as e:
            results['error'] = str(e)

        return results

    def _get_company_info(self, company_name: str) -> Dict:
        """Get company information from various sources."""
        # Simplified company info for demo
        return {
            'overview': f"{company_name} is an industry leader in technology innovation.",
            'values': ['Innovation', 'Excellence', 'Integrity'],
            'focus_areas': ['Technology', 'Innovation', 'Research']
        }

    def _search_company_news(self, company_name: str, max_results: int = 3) -> List[Dict]:
        """Search for recent company news."""
        # Simplified news for demo
        return [
            {
                'title': f'Latest Developments at {company_name}',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'summary': f'Recent technological advancements from {company_name}'
            }
        ]

    def get_structured_research(self, company_name: str) -> str:
        """Get research results in a structured format for the cover letter."""
        research = self.research_company(company_name)
        
        structured_info = []
        
        if research.get('overview'):
            structured_info.append(f"Company Overview: {research['overview']}")
        
        if research.get('focus_areas'):
            structured_info.append(f"Focus Areas: {', '.join(research['focus_areas'])}")
        
        if research.get('values'):
            structured_info.append(f"Company Values: {', '.join(research['values'])}")
        
        if research.get('recent_news'):
            news = research['recent_news'][0]
            structured_info.append(f"Recent Development: {news['title']} - {news['summary']}")
        
        return "\n\n".join(structured_info)

    def extract_company_name(self, job_description: str) -> str:
        """Extract company name from job description."""
        patterns = [
            r'position at (.*?)[\.,]',
            r'intern(?:ship)? at (.*?)[\.,]',
            r'role at (.*?)[\.,]',
            r'About (.*?):',
            r'About (.*?)\n',
            r'with (.*?)[\.,]',
            r'join (.*?)[\.,]'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE)
            if matches:
                company_name = matches[0].strip()
                # Clean up common suffixes
                company_name = re.sub(r'\b(inc|llc|corp|corporation)\b', '', company_name, flags=re.IGNORECASE)
                # Clean up any remaining punctuation
                company_name = re.sub(r'[^\w\s-]', '', company_name)
                return company_name.strip()
        
        return ""