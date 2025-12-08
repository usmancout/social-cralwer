
import json
from playwright.sync_api import sync_playwright

# from scrapers.example_scraper import ExampleScraper
from scrapers.behance_scraper import BehanceScraper


def main():

    scraper = BehanceScraper(username="grapheine")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(scraper.url)
        

        scraper.parse_page(page)
        

        print(json.dumps(scraper.data, indent=2))
        
        browser.close()


if __name__ == "__main__":
    main()
