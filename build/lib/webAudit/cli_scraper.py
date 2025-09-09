# cli_scraper.py
import asyncio
import sys
from .softbrowser import SoftBrowser
from .google_search_scraper import GoogleSearchScraper
from .page_scraper import PageScraper

async def main():
    if len(sys.argv) < 3:
        print("Usage: python cli_scraper.py <mode> <query_or_url> [selector_or_num_results]")
        print("Modes: google, page")
        return

    mode = sys.argv[1].lower()
    input_value = sys.argv[2]
    extra = sys.argv[3] if len(sys.argv) > 3 else None

    browser = SoftBrowser()
    try:
        if mode == "google":
            num_results = int(extra) if extra else 10
            scraper = GoogleSearchScraper(browser)
            results = await scraper.search(input_value, num_results)
            for r in results:
                print(f"{r['title']}\n{r['url']}\n{r['snippet']}\n---")

        elif mode == "page":
            selector = extra if extra else None
            scraper = PageScraper(browser)
            content = await scraper.scrape(input_value, selector)
            if isinstance(content, list):
                for c in content:
                    print(c)
            else:
                print(content)
        else:
            print("Invalid mode. Use 'google' or 'page'.")
    finally:
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
