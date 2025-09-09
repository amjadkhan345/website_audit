# softbrowser.py
import asyncio
from urllib.parse import quote
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

class SoftBrowser:
    def __init__(self, headless=True, timeout=30, user_agent=None):
        self.headless = headless
        self.timeout = timeout
        self.user_agent = user_agent or (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        )
        self.browser = None
        self.page = None
        self.dom = None
        self.url = None

    async def launch(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.page = await self.browser.new_page(user_agent=self.user_agent)
        return {"status": "success", "message": "Browser launched"}

    async def go(self, url: str):
        try:
            self.url = url
            await self.page.goto(url, timeout=self.timeout * 1000)
            html = await self.page.content()
            self.dom = BeautifulSoup(html, "html.parser")
            return {"status": "success", "url": url, "content": html, "error": None}
        except Exception as e:
            return {"status": "error", "url": url, "content": None, "error": str(e)}

    async def get_text(self, selector: str = None):
        if not self.dom:
            return {"status": "error", "error": "DOM not loaded"}
        try:
            if selector:
                elements = self.dom.select(selector)
                return [el.get_text(strip=True) for el in elements]
            return self.dom.get_text(strip=True)
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def fetch_multiple(self, urls: list):
        results = []
        for url in urls:
            result = await self.go(url)
            results.append(result)
        return results

    async def close(self):
        if self.browser:
            await self.browser.close()
        if hasattr(self, "playwright"):
            await self.playwright.stop()
        return {"status": "success", "message": "Browser closed"}
