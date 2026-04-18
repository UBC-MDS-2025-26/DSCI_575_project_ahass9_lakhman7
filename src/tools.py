import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(query, max_results=3):
    """
    Search the web for current information about a beauty product.
    
    Parameters
    ----------
    query : str
        The search query.
    max_results : int
        Maximum number of results to return.
    
    Returns
    -------
    str
        Formatted search results as a string.
    """
    results = tavily_client.search(query, max_results=max_results)
    snippets = []
    for r in results.get("results", []):
        snippets.append(
            f"Source: {r.get('url', 'N/A')}\n"
            f"Content: {r.get('content', 'N/A')}"
        )
    
    if not snippets:
        return "No web results found."
    
    return "\n\n".join(snippets)

if __name__ == "__main__":
    query = "best moisturizer for dry skin 2024"
    print(f"Searching for: {query}\n")
    results = web_search(query)
    print(results)