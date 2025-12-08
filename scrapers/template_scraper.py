

from playwright.sync_api import Page
from scrapers.base_scraper import BaseScraper


class TemplateScraper(BaseScraper):

    @property
    def url(self) -> str:
        """The URL to scrape"""
        return "https://example.com"
    
    @property
    def name(self) -> str:
        """Your scraper name"""
        return "MyScraperName"
    
    def parse_page(self, page: Page) -> None:
        """
        Extract data from the page.
        Store results in self.data
        """
        
        # Example: Get page title
        title = page.title()
        
        # Example: Get all links
        links = []
        for link in page.query_selector_all("a"):
            href = link.get_attribute("href")
            if href:
                links.append(href)
        
        # Example: Get text content
        body = page.query_selector("body")
        content = body.inner_text() if body else ""
        
        # Store the data
        self.data.append({
            "title": title,
            "url": page.url,
            "links": links,
            "content_preview": content[:200]
        })
        
        print(f"[{self.name}] Scraped: {title}")


# To use this scraper:
# 1. Copy this file
# 2. Change the class name, url, name, and parse_page logic
# 3. Import it in main.py
# 4. Run: python main.py
