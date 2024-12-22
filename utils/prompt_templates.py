def get_cover_letter_prompt(
    resume_text: str,
    job_description: dict,
    additional_content: list = None,
    portfolio_info: str = "",
    company_research: str = "",
    tone: str = "Professional",
    style: str = "Standard",
    company_name: str = ""
) -> str:

    # Extract exact education details
    education_section = resume_text.split('Education')[1].split('Experience')[0]
    
    prompt = f"""Write a cover letter that connects specific experiences to job requirements. Use ONLY these verified details:

EDUCATION (Use BOTH degrees):
{education_section}

VERIFIED TECHNICAL EXPERIENCE (Use specific details):
{resume_text.split('Experience')[1].split('Projects')[0]}

VERIFIED PROJECTS (Connect to job requirements):
{portfolio_info}

VERIFIED SKILLS:
- Languages: {resume_text.split('Languages:')[1].split('Frameworks:')[0]}
- Frameworks: {resume_text.split('Frameworks:')[1].split('Developer Tools:')[0]}
- Tools: {resume_text.split('Developer Tools:')[1].split('Strengths:')[0]}

JOB DETAILS:
{job_description['full_text']}
"""

    prompt += """
REQUIRED FORMAT:
1. First paragraph: Both degrees (Masters AND Bachelors)
2. Second paragraph: Graduate research experience with FPGA and machine learning work
3. Third paragraph: Relevant internship experiences
4. Fourth paragraph: Specific GitHub projects that demonstrate relevant skills
5. Final paragraph: Conclusion based on concrete skills

STRICT RULES:
1. NO mentions of AI/ML capabilities beyond NBA project and graduate research
2. NO generic phrases ("excited," "opportunity," "passionate")
3. NO claims about systems or frameworks not in resume
4. ONLY mention technologies listed in skills section
5. When mentioning GitHub projects, explain their relevance
6. Focus on actual achievements, not potential contributions

FORBIDDEN PHRASES - DO NOT USE:
- "excited to apply"
- "opportunity to contribute"
- "passionate about"
- "looking forward to"
- "AI agents"
- "context-aware systems"
- "multi-agent systems"

Example opening:
"As a Master's of Science student in Computer Science at USC (expected May 2026), building upon my Bachelor's in Informatics with Human-Computer Interaction specialization from UC Irvine (March 2023), I bring..."

[Write the letter focusing on concrete experience and demonstrated skills]"""

    return prompt