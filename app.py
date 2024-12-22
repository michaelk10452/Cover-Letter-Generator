import streamlit as st
from utils.document_processor import DocumentProcessor
from utils.llm_utils import OllamaLLM
from utils.prompt_templates import get_cover_letter_prompt
from utils.portfolio_agent import PortfolioAgent
from utils.research_agent import CompanyResearchAgent
import tempfile
import os

def main():
    st.title("Intelligent Cover Letter Generator")
    st.write("Upload your documents and provide relevant information to generate a personalized cover letter.")

    # Initialize processors
    doc_processor = DocumentProcessor()
    llm = OllamaLLM()
    research_agent = CompanyResearchAgent()
    portfolio_agent = PortfolioAgent()

    # Main Resume Upload
    st.subheader("Required Documents")
    resume_file = st.file_uploader("Upload your Resume (PDF format)", type=['pdf'])
    
    # Job description input
    job_description = st.text_area("Paste the Job Description", height=200)

    # Company Information
    company_name = st.text_input("Company Name", help="Enter the company name for the position")
    include_research = st.checkbox("Include company research in the cover letter", value=True)
    
    # Additional Documents Section
    st.subheader("Additional Information (Optional)")
    col1, col2 = st.columns(2)
    
    with col1:
        additional_docs = st.file_uploader(
            "Upload Additional Documents (transcripts, certifications, etc.)", 
            type=['pdf', 'doc', 'docx'], 
            accept_multiple_files=True
        )

    with col2:
        portfolio_links = st.text_area(
            "Enter your portfolio links (GitHub, Behance, etc.)\nOne link per line",
            placeholder="https://github.com/yourusername\nhttps://behance.net/yourusername"
        )
    
    # Style Preferences
    st.subheader("Style Preferences")
    col3, col4 = st.columns(2)
    with col3:
        tone = st.selectbox(
            "Select the tone of your cover letter",
            ["Professional", "Enthusiastic", "Confident", "Conservative"]
        )
    with col4:
        style = st.selectbox(
            "Select writing style",
            ["Standard", "Creative", "Technical", "Executive"]
        )

    if st.button("Generate Cover Letter") and resume_file and job_description and company_name:
        with st.spinner("Processing your documents..."):
            try:
                # Process resume
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(resume_file.getvalue())
                    resume_path = tmp_file.name
                resume_text = doc_processor.extract_text_from_pdf(resume_path)
                os.unlink(resume_path)

                # Process additional documents
                additional_content = []
                if additional_docs:
                    for doc in additional_docs:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                            tmp_file.write(doc.getvalue())
                            doc_path = tmp_file.name
                        content = doc_processor.extract_text_from_pdf(doc_path)
                        additional_content.append(content)
                        os.unlink(doc_path)

                # Process portfolio links
                portfolio_info = ""
                portfolio_details = None
                if portfolio_links:
                    with st.spinner("Analyzing portfolio information..."):
                        portfolio_info, portfolio_details = portfolio_agent.analyze_portfolio(portfolio_links.split('\n'))
                        
                        # Show portfolio analysis details
                        with st.expander("Portfolio Analysis Details", expanded=True):
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if portfolio_details['github_repos']:
                                    st.metric("GitHub Repositories", len(portfolio_details['github_repos']))
                            with col2:
                                if portfolio_details['behance_projects']:
                                    st.metric("Behance Projects", len(portfolio_details['behance_projects']))
                            with col3:
                                total_projects = len(portfolio_details['github_repos']) + len(portfolio_details['behance_projects'])
                                st.metric("Total Projects Found", total_projects)
                            
                            if portfolio_details['github_repos']:
                                st.subheader("🌟 GitHub Repositories Found")
                                for repo in portfolio_details['github_repos']:
                                    with st.container():
                                        st.markdown(f"### 📁 {repo['name']}")
                                        col4, col5 = st.columns([3, 1])
                                        with col4:
                                            st.write(f"**Description:** {repo['description']}")
                                            st.write(f"**Language:** {repo['language']}")
                                        with col5:
                                            st.write(f"**Stars:** {repo['stars']}")
                                            st.write(f"[View Repository]({repo['url']})")
                                        st.markdown("---")
                            
                            if portfolio_details['behance_projects']:
                                st.subheader("Behance Projects Found")
                                for project in portfolio_details['behance_projects']:
                                    st.write(f"🎨 {project['title']}")
                                    st.write(f"URL: {project['url']}")
                                    st.write("---")

                # Process job description
                processed_jd = doc_processor.process_job_description(job_description)

                # Company research
                company_research = ""
                if include_research and company_name:
                    with st.spinner("Researching company information..."):
                        company_research = research_agent.get_structured_research(company_name)
                        st.success(f"Researched company: {company_name}")
                
                # Generate prompt
                prompt = get_cover_letter_prompt(
                    resume_text=resume_text,
                    job_description=processed_jd,
                    additional_content=additional_content,
                    portfolio_info=portfolio_info,
                    company_research=company_research if include_research else "",
                    tone=tone,
                    style=style,
                    company_name=company_name
                )
                
                # Generate cover letter
                cover_letter = llm.generate_cover_letter(prompt)
                
                # Display results
                st.subheader("Generated Cover Letter")
                
                with st.expander("Sources Used", expanded=True):
                    st.write("Resume Content ✓")
                    if additional_content:
                        st.write("Additional Documents ✓")
                    if portfolio_info:
                        st.write("Portfolio Information ✓")
                        if portfolio_details and portfolio_details['github_repos']:
                            st.write("GitHub Projects Found ✓")
                    if company_research:
                        st.write("Company Research ✓")
                
                st.text_area("", cover_letter, height=400)
                
                # Export as PDF
                pdf_buffer = llm.export_to_pdf(cover_letter)
                
                # Download buttons
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="Download as Text",
                        data=cover_letter,
                        file_name="cover_letter.txt",
                        mime="text/plain"
                    )
                with col2:
                    st.download_button(
                        label="Download as PDF",
                        data=pdf_buffer,
                        file_name="cover_letter.pdf",
                        mime="application/pdf"
                    )
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()