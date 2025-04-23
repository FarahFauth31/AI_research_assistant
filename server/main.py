from fastapi import FastAPI, WebSocket
from server.pydantic_models.request_body import ChatBody
from server.services.web_search_service import WebSearchService
from server.services.relevant_sources_service import RelevantSourcesService
from server.services.gemini_service import GeminiService
import traceback
import asyncio

app = FastAPI()

search_service = WebSearchService()
relevant_sources_service = RelevantSourcesService()
gemini_service = GeminiService()

# Search query websocket to stream an LLM response based on the user's query
@app.websocket("/ws/search-query")
async def websocket_search_query_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        await asyncio.sleep(0.1)
        data = await websocket.receive_json()
        query = data.get("query")
        if not query:
            raise ValueError("Query is null.")
        search_results = search_service.web_search(query)
        relevant_results = relevant_sources_service.sort_sources(query, search_results)
        await asyncio.sleep(0.1)
        await websocket.send_json({
            "type": "search_result",
            "data": relevant_results
        })
        for chunk in gemini_service.generate_streamed_llm_response(query, relevant_results):
            await asyncio.sleep(0.1)
            await websocket.send_json({
                "type": "content",
                "data": chunk
            })
    except:
        print("Unexpected error occurred while streaming.")
        traceback.print_exc()
    finally:
        await websocket.close()

# Post request to get query from user and return an LLM-generatred answer to the query
@app.post("/search-query")
def search_query_endpoint(body: ChatBody):
    search_results = search_service.web_search(body.query)
    relevant_results = relevant_sources_service.sort_sources(body.query, search_results)
    llm_response = gemini_service.generate_llm_response(body.query, relevant_results)
    return llm_response