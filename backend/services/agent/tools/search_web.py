from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()

class SearchWebTool:
    """
    A tool for searching the web for relevant information on coding problems and algorithms.
    Uses SerpAPI to perform Google searches.
    """
    
    def __init__(self):
        self.api_key = os.environ.get('SERAPI_KEY')
        if not self.api_key:
            raise ValueError("SerpAPI key not found in environment variables. Set SERAPI_KEY in your .env file.")
    
    def search(self, query: str, num_results: int = 3):
        """
        Search the web for information related to a query.
        
        Args:
            query: The search query string
            num_results: The number of search results to return (default: 3)
            
        Returns:
            A string containing relevant information from web search results
        """
        search = GoogleSearch({
            "q": query, 
            "api_key": self.api_key, 
            "num": num_results,
            "hl": "en",  # Language for search results
            "gl": "us"   # Country for search results
        })
        
        results = search.get_dict()
        
        if "error" in results:
            return f"Error performing web search: {results['error']}"
        
        if "organic_results" not in results or len(results["organic_results"]) == 0:
            return f"No results found for query: '{query}'"
        
        formatted_results = []
        for i, item in enumerate(results["organic_results"], 1):
            title = item.get("title", "No title")
            link = item.get("link", "No link")
            snippet = item.get("snippet", "No description available")
            
            formatted_results.append(f"Result {i}:\nTitle: {title}\nURL: {link}\nDescription: {snippet}\n")
        
        return "\n".join(formatted_results)