import os
import sys
from google import genai
from google.genai import errors
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from config import Settings
import pydantic
import logging

settings = Settings()

class GeminiService:
    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API,
        )
        self.model = "gemini-2.0-flash"
    
    def return_full_prompt(self, query: str, search_results: list[dict]) -> str:
        if search_results:
            context_text = "\n\n".join([
                f"Source {i+1} {result['url']}:\n{result['content']}"
                for i, result in enumerate(search_results)
            ])
        else:
            context_text = "No context was found."
        
        full_prompt = f""""
        Context from web search:
        {context_text}

        Query: {query}

        Please provide a comprehensive, detailed, well-cited accurate response using the above conext. Think and reason deeply. Ensure it answers the query the user is asking. Do not use your own knowledge until it is absolutely necessary.
        """
        return full_prompt

    def generate_llm_response(self, query: str, search_results: list[dict]) -> str:
        full_prompt = self.return_full_prompt(query, search_results)

        try:
            response = self.client.models.generate_content(
                model=self.model, contents=full_prompt,
            )
            return response.text
        except (errors.APIError, errors.ClientError, errors.ServerError, 
        errors.UnknownFunctionCallArgumentError, errors.UnsupportedFunctionError,
        errors.FunctionInvocationError, pydantic.ValidationError) as e:
            logging.error(f"Error in Gemini Service: {type(e).__name__}: {e}", exc_info=True)
            return "No response could be created at this time."

    def generate_streamed_llm_response(self, query: str, search_results: list[dict]):
        full_prompt = self.return_full_prompt(query, search_results)

        try:
            response = self.client.models.generate_content_stream(
                model=self.model, contents=full_prompt,
            )
            for chunk in response:
                yield chunk.text

        except (errors.APIError, errors.ClientError, errors.ServerError, 
        errors.UnknownFunctionCallArgumentError, errors.UnsupportedFunctionError,
        errors.FunctionInvocationError, pydantic.ValidationError) as e:
            logging.error(f"Error in Gemini Service: {type(e).__name__}: {e}", exc_info=True)
            return "No response could be created at this time."


""" if __name__ == "__main__":
    llm_service = GeminiService()
    llm_service.generate_streamed_llm_response("hello", []) """