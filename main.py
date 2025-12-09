from playwright.sync_api import sync_playwright

from scrapers.behance_scraper import BehanceScraper
from scrapers.vimeo import vimeo


def main():

    scraper = BehanceScraper(username="Fiodor")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Only run login/session if scraper needs login
        if getattr(scraper, "requires_login", False):
            session = SessionManager(f"{scraper.__class__.__name__}_session.json.gz")
            session_loaded = session.load(page)

            page.goto(scraper.url)

            if not session_loaded:
                print(">> Please login manually, then press ENTER...")
                input()
                session.save(page)
            else:
                session.apply_storage(page)
        else:
            # Normal behaviour (like Vimeo)
            page.goto(scraper.url)


        scraper.parse_page(page)
        browser.close()


if __name__ == "__main__":
    main()
