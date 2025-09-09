# google_search_scraper.py
from urllib.parse import quote

from .softbrowser import SoftBrowser

class GoogleSearchScraper:
    def __init__(self, browser: SoftBrowser):
        self.browser = browser

    async def search(self, query: str, num_results=10):
        search_url = f"https://www.google.com/search?q={quote(query)}&num={num_results}"
        response = await self.browser.go(search_url)
    
        if response["status"] != "success":
            return [response] 
            
        else:
          return response
        """results = []
        for result in self._parse_google_html(response["content"]):
            results.append({
                "status": "success",
                "url": result["url"],
                "title": result["title"],
                "snippet": result.get("snippet", ""),
                "error": None
            })"""
          