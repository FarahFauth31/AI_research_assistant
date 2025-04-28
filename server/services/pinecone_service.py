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
from datetime import datetime

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


    def chunk_text_by_multi_paragraphs(self, text: str, max_chunk_size: int = 1500, min_chunk_size: int = 500) -> list[str]:
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
    
    def embed_chunks(self, chunks: list[str]) -> list:
        logging.info("vectorizing now...")
        vectorized_chunks = []
        for chunk in chunks:
            embedding = self.embedding_model.encode(chunk)
            vectorized_chunks.append(embedding)
        return vectorized_chunks
    
    def upsert(self, chunks: list[str], vectorized_chunks, name_doc: str, namespace: str = "ns2"):
        logging.info("saving vectors...")
        vectors=[]
        for i, (vec, chunk_text) in enumerate(zip(vectorized_chunks, chunks)):
            vector_dict = {
                "id": f"{name_doc}_chunk{i}",
                "values": vec,
                "metadata": {"text": chunk_text}
            }
            vectors.append(vector_dict)

        self.index.upsert(
            vectors=vectors,
            namespace=namespace
        )
    
    def retrieve_results(self, query: str, namespace: str = "ns2"):
        retrieved_results = []
        query_embedding = self.embedding_model.encode(query).tolist()
        results = self.index.query(
            namespace=namespace,
            top_k=5,
            include_values=True,
            include_metadata=True,
            vector=query_embedding
        )
        if results['matches']:
            for match in results['matches']:
                if match.get('score', 0) > 0.7:
                    result_dict = {
                        "id": match.get('id', 0),
                        "score": match.get('score', 0),
                        "text": match.get('metadata', None).get('text', "")
                    }
                    retrieved_results.append(result_dict)
        return retrieved_results
        
    def store_search_results(self, text: str):
        chunks = self.chunk_text_by_multi_paragraphs(text)
        embeddings = self.embed_chunks(chunks)
        self.upsert(chunks, embeddings, datetime.now())


if __name__ == "__main__":
    db = PineconeDB()
    db.store_search_results("What are you doing?")
    """ text_doc = db.parse_pdf(file_path="/home/farah/Desktop/git_ai_research_assistant/a-practical-guide-to-building-agents.pdf")
    chunks = db.chunk_text_by_multi_paragraphs(text_doc)
    embeddings = db.embed_chunks(chunks)
    db.upsert(chunks=chunks, vectorized_chunks=embeddings, name_doc="OpenAI_ai_agent_guide") """