# softbrowser.py
import asyncio
import httpx
import quickjs
from bs4 import BeautifulSoup
#from py_mini_racer import py_mini_racer
from urllib.parse import urljoin, quote

class SoftBrowser:
    def __init__(self, user_agent=None, timeout=30):
        self.timeout = timeout
        #self.js_ctx = py_mini_racer.MiniRacer()
        self.js_ctx = quickjs.Context()
        self.dom = None
        self.url = None
        self.user_agent = user_agent or (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        )
        self.client = httpx.AsyncClient(
            headers={
                "User-Agent": self.user_agent,
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Referer": "https://www.google.com/"
            },
            timeout=self.timeout
        )

    async def go(self, url: str):
        try:
            # fetch page
            self.url = url
            html = await self._fetch(url)
            self.dom = html
            return {"status": "success", "url": url, "content": html, "error": None}
        except Exception as e:
            return {"status": "error", "url": url, "content": None, "error": str(e)}

    async def _fetch(self, url: str) -> str:
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.RequestError as e:
            raise RuntimeError(f"Network error while fetching {url}: {e}")

    def _render(self, html: str):
        self.dom = BeautifulSoup(html, "html.parser")

    def query_selector(self, selector: str):
        if not self.dom:
            raise RuntimeError("DOM not loaded. Call go(url) first.")
        return self.dom.select(selector)

    def get_html(self) -> str:
        if not self.dom:
            raise RuntimeError("DOM not loaded.")
        return str(self.dom)

    def get_text(self, selector: str = None):
        if not self.dom:
            raise RuntimeError("DOM not loaded.")
        if selector:
            elements = self.query_selector(selector)
            return [el.get_text(strip=True) for el in elements]
        return self.dom.get_text(strip=True)

    async def close(self):
        await self.client.aclose()
