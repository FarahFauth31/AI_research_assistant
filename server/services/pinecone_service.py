from pinecone import Pinecone
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from config import Settings
from google import genai
from llama_cloud_services import LlamaParse
from sentence_transformers import SentenceTransformer
import pydantic
import logging

settings = Settings()

class PineconeDB:
    def __init__(self, index_name="ai-assistant-gemini-embed-index1"):
        self.pc = Pinecone(api_key=settings.PINECONE_API)
        self.index = self.pc.Index(index_name)
        self.embedding_model = SentenceTransformer("multi-qa-distilbert-cos-v1")


    def parse_pdf(self, file_path: str) -> str:
        parser = LlamaParse(
            api_key=settings.LLAMA_INDEX_API,
            num_workers=1,     
            verbose=True,
            language="en",
        )
        result = parser.parse(file_path)
        text_document = result.get_text_documents(split_by_page=False)
        return text_document[0].text


    def chunk_text_by_multi_paragraphs(self, text: str, max_chunk_size: int = 200, min_chunk_size: int = 100) -> list[str]:
        """
        Split text into chunks at paragraph boundaries while respecting min and max chunk sizes.
        
        Args:
            text: The input text to be split
            max_chunk_size: The maximum size of each chunk
            min_chunk_size: The minimum size of each chunk
        
        Returns:
            A list of text chunks
        """
        chunks = []
        current_chunk = ""
        
        start_index = 0
        while start_index < len(text):
            end_index = start_index + max_chunk_size
            
            if end_index >= len(text):
                end_index = len(text)
            else:
                # Find the nearest paragraph boundary
                paragraph_boundary = text.find("\n\n", end_index)
                if paragraph_boundary != -1:
                    end_index = paragraph_boundary
            
            chunk = text[start_index:end_index].strip()
            
            if len(chunk) >= min_chunk_size:
                chunks.append(chunk)
                current_chunk = ""
            else:
                current_chunk += chunk + "\n\n"
            
            start_index = end_index + 1
        
        # Handle any remaining text in current_chunk
        if len(current_chunk) >= min_chunk_size:
            chunks.append(current_chunk.strip())
        elif chunks:
            chunks[-1] += "\n\n" + current_chunk.strip()
        else:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def embed_chunks(self, chunks: list[str]):
        print("vectorizing now...")
        vectorized_chunks = []
        for chunk in chunks:
            embedding = self.embedding_model.encode(chunk)
            vectorized_chunks.append(embedding)
        return vectorized_chunks


    


"""

index.upsert(

    vectors=[

        {

            "id": "vec1", 

            "values": [1.0, 1.5], 

            "metadata": {"genre": "drama"}

        }, {

            "id": "vec2", 

            "values": [2.0, 1.0], 

            "metadata": {"genre": "action"}

        }, {

            "id": "vec3", 

            "values": [0.1, 0.3], 

            "metadata": {"genre": "drama"}

        }, {

            "id": "vec4", 

            "values": [1.0, -2.5], 

            "metadata": {"genre": "action"}

        }

    ],

    namespace= "ns1"

) """

if __name__ == "__main__":
    db = PineconeDB()
    text_doc = db.parse_pdf(file_path="/home/farah/Desktop/git_ai_research_assistant/a-practical-guide-to-building-agents.pdf")
    chunks = db.chunk_text_by_multi_paragraphs(text_doc)
    embeddings = db.embed_chunks(chunks)
    print(embeddings)