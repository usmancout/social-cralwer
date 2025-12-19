from playwright.sync_api import sync_playwright
from cross_platform_mapping import cross_platform_mapper
from login_session.session_manager import SessionManager
from scrapers.instagram import instagram
from scrapers._facebook import FacebookScraper


def run_scraper(scraper, page):
    print(f"\n>> Running scraper: {scraper.__class__.__name__}")

    # IMPORTANT: Navigate first so localStorage is accessible
    page.goto(scraper.base_url, wait_until="domcontentloaded")

    # Handle login (only if scraper requires it)
    if getattr(scraper, "requires_login", False):
        session = SessionManager(f"{scraper.__class__.__name__}_session.json.gz")
        loaded = session.load(page)

        if not loaded:
            print(">> Login required. Please log in manually, then press ENTER...")
            input()
            session.save(page)
        else:
            session.apply_storage(page)
            page.reload()  # Apply restored session properly

    scraper.parse_page(page)
    print(f">> Finished: {scraper.__class__.__name__}")


def main():
    scrapers = [
        instagram(username="nazarali870"),
        FacebookScraper(username="profile.php?id=100081288807680&sk"),
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for scraper in scrapers:
            run_scraper(scraper, page)

        browser.close()

        cross_platform_mapper.print_all_cards()
        cross_platform_mapper.compare_following_across_platforms()
        cross_platform_mapper.group_following_across_all_platforms()


if __name__ == "__main__":
    main()
