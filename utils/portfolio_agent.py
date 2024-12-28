import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
from urllib.parse import urlparse
import re
import streamlit as st
from config import RESEARCH_SETTINGS

class PortfolioAgent:
    def __init__(self):
        self.headers = {'User-Agent': RESEARCH_SETTINGS['user_agent']}



    def analyze_portfolio(self, urls: List[str]) -> Tuple[str, Dict]:
        """Analyze portfolio links and extract relevant information."""
        portfolio_info = []
        analysis_details = {
            'github_repos': [],
            'behance_projects': [],
            'other_links': []
        }
        
        for url in urls:
            url = url.strip()
            if not url:
                continue
                
            domain = urlparse(url).netloc
            
            if 'github.com' in domain:
                print(f"\nAnalyzing GitHub profile: {url}")
                info, repos = self._analyze_github(url)
                if info:
                    portfolio_info.append(info)
                    analysis_details['github_repos'].extend(repos)
                    print(f"Added {len(repos)} repositories to analysis")
            elif 'behance.net' in domain:
                info, projects = self._analyze_behance(url)
                if info:
                    portfolio_info.append(info)
                    analysis_details['behance_projects'].extend(projects)
            else:
                analysis_details['other_links'].append(url)
                    
        return "\n\n".join(filter(None, portfolio_info)), analysis_details

    def _analyze_github(self, url: str) -> Tuple[str, List[Dict]]:
        """Analyze GitHub profile and repositories."""
        try:
            # Extract username from URL
            username = url.split('github.com/')[-1].split('/')[0]
            
            # Get public repositories
            api_url = f"https://api.github.com/users/{username}/repos"
            print(f"Attempting to fetch GitHub repos for user: {username}")
            response = requests.get(api_url)
            
            if response.status_code != 200:
                print(f"Error fetching GitHub repos: Status code {response.status_code}")
                return "", []
                
            repos = response.json()
            print(f"Successfully fetched GitHub data. Found {len(repos)} repositories")
            
            # Filter and analyze repositories
            relevant_repos = []
            for repo in repos:
                if not repo['fork']:  # Only include original repos
                    relevant_repos.append({
                        'name': repo['name'],
                        'description': repo['description'] or "No description provided",
                        'stars': repo['stargazers_count'],
                        'language': repo['language'] or "Not specified",
                        'url': repo['html_url']
                    })
            
            if not relevant_repos:
                print("No relevant repositories found")
                return "", []
                
            # Format the information
            repo_info = []
            for repo in relevant_repos:
                if repo['description']:
                    repo_info.append(f"- {repo['name']}: {repo['description']} ({repo['language']})")
            
            if repo_info:
                return "GitHub Projects:\n" + "\n".join(repo_info), relevant_repos
            
        except Exception as e:
            print(f"Error analyzing GitHub profile: {str(e)}")
            
        return "", []

    def _analyze_behance(self, url: str) -> Tuple[str, List[Dict]]:
        """Analyze Behance portfolio."""
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                return "", []
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            projects = []
            project_elements = soup.find_all('div', class_='Project-title')
            
            project_info = []
            for element in project_elements[:3]:
                title = element.get_text().strip()
                if title:
                    project_info.append({
                        'title': title,
                        'url': url
                    })
                    projects.append(f"- {title}")
            
            if projects:
                return "Design Projects:\n" + "\n".join(projects), project_info
                
        except Exception as e:
            st.error(f"Error analyzing Behance profile: {str(e)}")
            
        return "", []

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,;:-]', '', text)
        return text.strip()