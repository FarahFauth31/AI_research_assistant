import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from config import Settings
from tavily import TavilyClient
import trafilatura
import logging

settings = Settings()
tavily_client = TavilyClient(api_key = settings.TAVILY_API)

class WebSearchService:
    """This service employs the Tavily API to find relevant sources to the user specified query."""
    def web_search(self, query: str):
        results = []
        try:
            response = tavily_client.search(query, max_results=1, search_depth="basic", chunks_per_source=1)
            search_results = response.get("results", [])

            for result in search_results:
                downloaded_content = trafilatura.fetch_url(result.get('url'))
                if downloaded_content:
                    content = trafilatura.extract(downloaded_content, include_comments=False)
                else:
                    content = ""
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": content or "",
                })
            return results
        
        except Exception as e:
            logging.error(f"Unexpected error in Search Service occurred: {e}", exc_info=True)
            return []
        
if __name__ == "__main__":
    search_service = WebSearchService()
    search_service.web_search("""

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec viverra ante non neque facilisis suscipit. Phasellus quis massa odio. Ut venenatis elit sit amet nunc tempor, ut porttitor diam ultricies. Curabitur aliquam ligula nibh, et lacinia ante aliquet nec. In at mi non metus facilisis sodales. Quisque tempor nibh id leo mollis, ac malesuada massa tempus. Mauris euismod augue in urna ultrices posuere.

Fusce pulvinar mauris vel orci imperdiet, vel pretium urna dignissim. Aenean ut arcu tincidunt, facilisis risus sit amet, pellentesque est. Integer lacus magna, tempor eget eros vitae, pharetra imperdiet mi. Nulla dignissim enim et diam pulvinar malesuada. Aliquam ut hendrerit nulla. Vivamus ac vulputate arcu, quis facilisis urna. Sed hendrerit rutrum mi, ornare dapibus leo. Cras ac ante volutpat arcu suscipit placerat. Phasellus commodo massa sed arcu vulputate fringilla. Nulla ullamcorper dolor ut sodales lobortis.

Morbi cursus lacus sed augue vestibulum bibendum. Nulla ut diam tortor. In bibendum tortor nunc, vitae vehicula felis elementum ac. Proin feugiat purus et ligula semper, at egestas dui tempus. Nulla venenatis bibendum orci non tempus. Proin sollicitudin vel diam a blandit. Donec vehicula varius ex, eu varius lectus hendrerit quis. In non pellentesque mauris. Proin id laoreet elit, vel gravida erat. Proin fermentum, orci id vestibulum ornare, mauris tortor blandit velit, non maximus turpis metus quis eros. Ut vel convallis lacus. Sed aliquet nulla neque, non feugiat odio tincidunt eu.

Ut aliquet justo et enim efficitur, ut tempus ipsum tempus. Aenean vel nisl et neque mattis pulvinar eu vitae leo. Proin malesuada enim quis libero posuere consequat. Nulla ultrices aliquam vestibulum. Sed facilisis arcu sed malesuada ornare. Nam nec elementum mi. Donec nunc ex, maximus at arcu eu, consectetur pretium odio. Morbi enim sapien, dapibus at nisl ullamcorper, dapibus pretium orci. Vestibulum aliquam blandit mollis. Ut viverra lectus sed ante hendrerit, non sollicitudin erat scelerisque. Nunc vitae fermentum ex. Nullam ac cursus nunc. Vestibulum lectus sapien, ultrices et tristique at, rutrum a orci. Aliquam sit amet diam placerat, sollicitudin ipsum quis, bibendum eros.

Vivamus sit amet lectus lacus. Suspendisse vitae fermentum justo. Integer eget faucibus mauris. Mauris ultrices sed dolor convallis iaculis. Donec aliquam vel nisl id cursus. Nunc eget nunc fermentum, pulvinar ex eget, molestie velit. Maecenas fringilla ipsum eget ex interdum, sit amet porta erat bibendum. Aliquam non cursus lectus. Praesent cursus nisl at elit lacinia, ut maximus ipsum scelerisque. Fusce in mollis libero. Etiam auctor ullamcorper ligula, et eleifend turpis scelerisque aliquam. Mauris ultricies imperdiet quam at condimentum. """)