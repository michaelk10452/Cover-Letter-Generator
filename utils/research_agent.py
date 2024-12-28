import requests
from bs4 import BeautifulSoup
from typing import Dict, List
import json
from datetime import datetime
import re
import nltk
from config import RESEARCH_SETTINGS
import os
import time

class CompanyResearchAgent:
    def __init__(self):
        try:
            nltk.data.find('punkt')
        except LookupError:
            nltk.download('punkt')
        
        self.headers = {'User-Agent': RESEARCH_SETTINGS['user_agent']}
        self.cache_dir = RESEARCH_SETTINGS['cache_dir']
        os.makedirs(self.cache_dir, exist_ok=True)

    def research_company(self, company_name: str) -> Dict:
        """Research company using web scraping and news API."""
        print(f"\n[Research] Starting research for company: {company_name}")
        cache_file = os.path.join(self.cache_dir, f"{company_name.lower().replace(' ', '_')}.json")
        
        # Check cache
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                data = json.load(f)
                if time.time() - data['timestamp'] < RESEARCH_SETTINGS['cache_expiration']:
                    print("[Research] Using cached data")
                    return data['content']

        try:
            # Get company info from website first
            company_info = self._get_company_info(company_name)
            print("[Research] Company info retrieved")

            # Get company news
            news = self._get_company_news(company_name)
            print(f"[Research] News articles retrieved: {len(news)}")

            research = {
                'company_name': company_name,
                'overview': company_info.get('overview', ''),
                'recent_news': news,
                'values': company_info.get('values', []),
                'focus_areas': company_info.get('focus_areas', []),
                'error': None
            }

            # Cache the results
            with open(cache_file, 'w') as f:
                json.dump({
                    'timestamp': time.time(),
                    'content': research
                }, f)

            return research

        except Exception as e:
            print(f"[Research] Error occurred: {str(e)}")
            return self._get_fallback_data(company_name, str(e))

    def _get_company_news(self, company_name: str) -> List[Dict]:
        """Get company news from NewsAPI."""
        try:
            url = 'https://newsapi.org/v2/everything'
            params = {
                'q': company_name,
                'sortBy': 'publishedAt',
                'apiKey': RESEARCH_SETTINGS['news_api_key'],
                'language': 'en',
                'pageSize': RESEARCH_SETTINGS['max_news_results']
            }
            print("[Research] Requesting news articles")
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                news_data = response.json()
                if news_data.get('articles'):
                    articles = []
                    for article in news_data['articles'][:3]:
                        if article.get('title') and article.get('description'):
                            articles.append({
                                'title': article['title'],
                                'summary': article['description'],
                                'date': article['publishedAt']
                            })
                    print(f"[Research] Found {len(articles)} relevant news articles")
                    return articles
        except Exception as e:
            print(f"[Research] Error fetching news: {str(e)}")
        return []

    def _get_company_info(self, company_name: str) -> Dict:
        """Get company information through web search and scraping."""
        try:
            search_url = f"https://www.google.com/search?q={company_name}+company+about"
            response = requests.get(search_url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            company_info = {
                'overview': '',
                'values': [],
                'focus_areas': []
            }

            # Extract from search results directly
            for result in soup.find_all('div', class_='BNeawe'):
                text = result.get_text()
                if len(text) > 100:  # Likely a meaningful description
                    company_info['overview'] = text
                    break

            print(f"[Research] Company overview length: {len(company_info['overview'])}")
            return company_info

        except Exception as e:
            print(f"[Research] Error scraping company info: {str(e)}")
            return {}

    def _get_fallback_data(self, company_name: str, error: str = None) -> Dict:
        """Provide fallback data when research fails."""
        print("[Research] Using fallback data")
        return {
            'company_name': company_name,
            'overview': f"{company_name} is a company focused on innovation and technology solutions.",
            'recent_news': [],
            'values': ["Innovation", "Excellence", "Integrity"],
            'focus_areas': ["Technology", "Innovation", "Research"],
            'error': error
        }

    def get_structured_research(self, company_name: str) -> str:
        """Format research results for the cover letter."""
        print(f"\n[Research] Formatting research for {company_name}")
        research = self.research_company(company_name)
        
        sections = []
        
        if research.get('overview'):
            sections.append(f"Company Overview: {research['overview']}")
            print(f"[Research] Overview added ({len(research['overview'])} chars)")
        
        if research.get('values'):
            sections.append(f"Company Values: {', '.join(research['values'])}")
            print(f"[Research] Values added: {research['values']}")
        
        if research.get('focus_areas'):
            sections.append(f"Focus Areas: {', '.join(research['focus_areas'])}")
            print(f"[Research] Focus areas added: {research['focus_areas']}")
        
        if research.get('recent_news'):
            latest_news = research['recent_news'][0]
            sections.append(f"Recent Development: {latest_news['title']}")
            print(f"[Research] Latest news added: {latest_news['title']}")
        
        formatted_research = "\n\n".join(sections)
        print("\n[Research] Final formatted research:")
        print(formatted_research)
        
        return formatted_research