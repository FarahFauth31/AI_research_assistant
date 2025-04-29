import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from services.gemini_service import GeminiService
from google.genai import errors

class TestGeminiService(unittest.TestCase):
    """Test cases for the GeminiService class"""

    def setUp(self):
        self.client_patch = patch('google.genai.Client')
        self.mock_client = self.client_patch.start()
        self.gemini_service = GeminiService()
        self.gemini_service.client = MagicMock()
        self.query = "What is Machine Learning?"
        self.search_results = [
            {
                "title": "Introduction to Machine Learning",
                "url": "https://example.com/ml-intro",
                "content": "Machine learning is a branch of artificial intelligence."
            },
            {
                "title": "Machine Learning Algorithms",
                "url": "https://example.com/ml-algorithms",
                "content": "Common ML algorithms include linear regression, decision trees, and neural networks."
            }
        ]

    def tearDown(self):
        self.client_patch.stop()

    def test_return_full_prompt(self):
        """Test that the full prompt is correctly constructed"""
        prompt = self.gemini_service.return_full_prompt(self.query, self.search_results)
        
        self.assertIn(self.query, prompt)
        for result in self.search_results:
            self.assertIn(result["content"], prompt)
            self.assertIn(result["url"], prompt)
        
        self.assertIn("Context from web search:", prompt)
        self.assertIn("Query:", prompt)

    def test_return_full_prompt_no_results(self):
        """Test prompt construction when no search results are available"""
        prompt = self.gemini_service.return_full_prompt(self.query, [])
        
        self.assertIn("No context was found.", prompt)
        self.assertIn(self.query, prompt)

    def test_generate_llm_response_success(self):
        """Test successful LLM response generation"""
        mock_response = MagicMock()
        mock_response.text = "Machine learning is a field of study that gives computers the ability to learn without being explicitly programmed."
        
        self.gemini_service.client.models.generate_content.return_value = mock_response
        
        response = self.gemini_service.generate_llm_response(self.query, self.search_results)
        
        self.assertEqual(response, mock_response.text)
        
        self.gemini_service.client.models.generate_content.assert_called_once()
        call_args = self.gemini_service.client.models.generate_content.call_args
        self.assertEqual(call_args[1]['model'], "gemini-2.0-flash")
        self.assertIn(self.query, call_args[1]['contents'])

    def test_generate_llm_response_api_error(self):
        """Test handling of API errors during response generation"""
        pass

    def test_generate_streamed_llm_response(self):
        """Test streaming LLM response generation"""
        pass

if __name__ == '__main__':
    unittest.main()