# google_search_scraper.py
from urllib.parse import quote
from .softbrowser import SoftBrowser
class GoogleSearchScraper:
    def __init__(self):
        browser = SoftBrowser(headless=True)
        await browser.launch()
        self.browser = browser  # Instance of SoftBrowser

    async def search(self, query: str, num_results=10):
        try:
            search_url = f"https://www.google.com/search?q={quote(query)}&num={num_results}"
            result = await self.browser.go(search_url)
            if result["status"] != "success":
                return {"status": "error", "query": query, "results": None, "error": result["error"]}

            # Extract search results from DOM
            elements = self.browser.dom.select("div#search .g")
            results = []
            for el in elements:
                title = el.select_one("h3")
                link = el.select_one("a")
                desc = el.select_one(".VwiC3b")
                results.append({
                    "title": title.get_text(strip=True) if title else "",
                    "url": link["href"] if link else "",
                    "description": desc.get_text(strip=True) if desc else ""
                })
            return {"status": "success", "query": query, "results": results, "error": None}

        except Exception as e:
            return {"status": "error", "query": query, "results": None, "error": str(e)}
