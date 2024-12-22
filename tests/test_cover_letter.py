import unittest
from utils.document_processor import DocumentProcessor
from utils.llm_utils import OllamaLLM
from utils.qa_utils import QualityChecker
import os
import tempfile

class TestCoverLetterGenerator(unittest.TestCase):
    def setUp(self):
        self.doc_processor = DocumentProcessor()
        self.llm = OllamaLLM()
        self.qa_checker = QualityChecker()
        
        # Create test data
        self.test_resume = """
        John Doe
        Software Engineer
        
        Experience:
        - Senior Developer at Tech Corp
        - Led team of 5 engineers
        - Implemented CI/CD pipeline
        """
        
        self.test_job_description = """
        Software Engineer Position
        
        Requirements:
        - 5+ years experience
        - Python expertise
        - Team leadership
        
        Responsibilities:
        - Lead development team
        - Implement best practices
        """

    def test_document_processor(self):
        # Test PDF creation and reading
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
            tmp.write(self.test_resume.encode())
            tmp.flush()
            
            # Test text extraction
            extracted_text = self.doc_processor._clean_text(self.test_resume)
            self.assertIsNotNone(extracted_text)
            self.assertTrue(len(extracted_text) > 0)
            
            os.unlink(tmp.name)

    def test_job_description_processing(self):
        processed_jd = self.doc_processor.process_job_description(self.test_job_description)
        
        # Check if all required fields are present
        self.assertIn('requirements', processed_jd)
        self.assertIn('responsibilities', processed_jd)
        self.assertIn('skills', processed_jd)
        
        # Check if requirements were extracted
        self.assertTrue(len(processed_jd['requirements']) > 0)

    def test_quality_checker(self):
        test_letter = """
        Dear Hiring Manager,
        
        I am writing to express my interest in the Software Engineer position.
        As a detail-oriented team player, I would be a great fit.
        
        Sincerely,
        John Doe
        """
        
        quality_results = self.qa_checker.analyze_cover_letter(test_letter)
        
        # Check if analysis contains all required fields
        self.assertIn('ai_patterns_detected', quality_results)
        self.assertIn('cliches_found', quality_results)
        self.assertIn('readability_score', quality_results)
        self.assertIn('suggestions', quality_results)
        
        # Check if AI patterns were detected
        self.assertTrue(len(quality_results['ai_patterns_detected']) > 0)
        
        # Check if clichés were found
        self.assertTrue(len(quality_results['cliches_found']) > 0)

    def test_llm_connection(self):
        try:
            model_info = self.llm.get_model_info()
            self.assertIsNotNone(model_info)
        except Exception as e:
            self.fail(f"LLM connection failed: {str(e)}")

if __name__ == '__main__':
    unittest.main()