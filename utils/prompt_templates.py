def _get_tone_guidelines(tone: str) -> str:
    """Provides specific guidelines based on the selected tone."""
    guidelines = {
        "Professional": """
- Use formal language and industry-standard terminology
- Focus on measurable achievements and concrete skills
- Maintain objectivity and clarity
- Use precise, direct statements""",
        
        "Enthusiastic": """
- Emphasize positive outcomes and achievements
- Show genuine interest in specific projects and technologies
- Use active, energetic language while maintaining professionalism
- Highlight collaborative successes""",
        
        "Confident": """
- Lead with strong action verbs
- Emphasize leadership and initiative
- Focus on quantifiable achievements
- Use assertive but not aggressive language""",
        
        "Conservative": """
- Use traditional business language
- Maintain formal tone throughout
- Focus on established achievements
- Keep descriptions straightforward and factual"""
    }
    return guidelines.get(tone, guidelines["Professional"])

def _get_style_guidelines(style: str) -> str:
    """Provides specific guidelines based on the selected writing style."""
    guidelines = {
        "Standard": """
- Clear, straightforward writing
- Balanced mix of technical and business language
- Traditional business letter structure
- Focus on relevant achievements""",
        
        "Technical": """
- Emphasize technical skills and achievements
- Use industry-specific terminology
- Include specific technologies and methodologies
- Focus on technical problem-solving examples""",
        
        "Creative": """
- Use descriptive language while maintaining professionalism
- Highlight innovative problem-solving
- Emphasize unique approaches and solutions
- Focus on creative achievements""",
        
        "Executive": """
- Focus on leadership and strategic thinking
- Emphasize high-level impact
- Use business-focused language
- Highlight organizational impact"""
    }
    return guidelines.get(style, guidelines["Standard"])

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
    """
    Generates a prompt for cover letter creation based on provided information and preferences.
    """
    print(f"\n[Debug] Processing cover letter for {company_name}")
    
    # Extract sections from resume
    education_section = resume_text.split('Education')[1].split('Experience')[0] if 'Education' in resume_text else ""
    experience_section = resume_text.split('Experience')[1].split('Projects')[0] if 'Experience' in resume_text else ""
    
    # Try to extract skills sections if they exist
    skills_section = ""
    try:
        skills_parts = []
        sections = ['Languages:', 'Frameworks:', 'Developer Tools:']
        for i, section in enumerate(sections):
            if section in resume_text:
                next_section = sections[i + 1] if i + 1 < len(sections) else 'Strengths:'
                skills_parts.append(f"{section} {resume_text.split(section)[1].split(next_section)[0].strip()}")
        skills_section = "\n".join(skills_parts)
    except (IndexError, KeyError):
        print("[Debug] Could not extract skills section")
        pass

    # Print debug information
    print("\n[Debug] Prompt Components:")
    print(f"Education Section Length: {len(education_section)} chars")
    print(f"Experience Section Length: {len(experience_section)} chars")
    print(f"Skills Section Length: {len(skills_section)} chars")
    print(f"Company Research Length: {len(company_research)} chars")
    
    prompt = f"""Write a professional cover letter using the following verified information and guidelines:

VERIFIED INFORMATION:
1. Education Background:
{education_section}

2. Professional Experience:
{experience_section}

3. Technical Skills:
{skills_section}

4. Portfolio Projects:
{portfolio_info}

5. Company Research:
{company_research}

6. Job Details:
{job_description['full_text']}

TONE AND STYLE GUIDELINES:
- Use a {tone.lower()} tone throughout the letter
- Follow a {style.lower()} writing style
- When referencing company information, use ONLY facts from the company research above
- Do not fabricate or assume additional company information
- Reference at most one recent company development or news item
- Focus on matching your experience to the company's verified focus areas

For {tone.lower()} tone, this means:
{_get_tone_guidelines(tone)}

For {style.lower()} style, this means:
{_get_style_guidelines(style)}

REQUIRED FORMAT:
Note: Do not include any address or greeting - these will be added automatically.
1. First paragraph (2-3 sentences): Briefly introduce your educational background and ONE specific reason for interest based on the company research
2. Body paragraphs (2-3 paragraphs, each 3-4 sentences): Focus on your most relevant experiences that match the job requirements
3. Final paragraph (2-3 sentences): Summarize your key qualifications that match the role requirements

STRICT RULES:
1. Keep the letter concise - maximum 5 paragraphs total
2. Focus only on experiences and skills that directly match the job requirements
3. Do not use any generic enthusiasm or filler phrases
4. End with concrete qualifications, not expressions of interest
5. Do not repeat information between paragraphs
6. Only include company information that was provided in the research section
7. Do not make assumptions about the company beyond the provided research
8. Do not include any contact information or signature - this will be added automatically

FORBIDDEN PHRASES AND CONTENT:
- Any expression of excitement or eagerness
- Future speculations about the company
- Unverified company information
- Generic industry trends
- Market predictions or analysis
- References to news not included in the research
- Generic phrases about company reputation
- Vague statements about company culture
- Personal opinions about the company's status or future

[Write a focused, specific cover letter that demonstrates concrete qualifications while maintaining the specified tone and style.]"""

    print("\n[Debug] Prompt Generated:")
    print(f"Tone: {tone}")
    print(f"Style: {style}")
    print(f"Prompt Length: {len(prompt)} chars")
    
    return prompt