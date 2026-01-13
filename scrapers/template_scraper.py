from playwright.sync_api import Page
from scrapers.base_scraper import BaseScraper


class TemplateScraper(BaseScraper):

    @property
    def url(self) -> str:
        return "https://example.com"

    @property
    def name(self) -> str:
        return "MyScraperName"

    def parse_page(self, page: Page) -> None:
        title = page.title()

        links = []
        for link in page.query_selector_all("a"):
            href = link.get_attribute("href")
            if href:
                links.append(href)

        body = page.query_selector("body")
        content = body.inner_text() if body else ""

        self.data.append({
            "title": title,
            "url": page.url,
            "links": links,
            "content_preview": content[:200]
        })

        print(f"[{self.name}] Scraped: {title}")
