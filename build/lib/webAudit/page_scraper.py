# page_scraper.py
from .softbrowser import SoftBrowser

class PageScraper:
    def __init__(self, browser: SoftBrowser):
        self.browser = browser

    async def scrape(self, url: str, selector: str = None):
        
        response = await self.browser.go(url)
        if response["status"] != "success":
            return response  # return JSON with error
    
        content = self._extract_content(response["content"], selector)
        return {"status": "success", "url": url, "content": content, "error": None}