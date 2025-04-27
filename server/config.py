from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    TAVILY_API: str = ""
    GEMINI_API: str = ""
    PINECONE_API: str = ""
    LLAMA_INDEX_API: str = ""