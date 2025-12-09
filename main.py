from playwright.sync_api import sync_playwright

from scrapers.behance_scraper import BehanceScraper
from scrapers.vimeo import vimeo


def main():

    scraper = BehanceScraper(username="Fiodor")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(scraper.url)
        scraper.parse_page(page)
        browser.close()

if __name__ == "__main__":
    main()
