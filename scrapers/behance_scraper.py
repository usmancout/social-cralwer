
import time
from playwright.sync_api import Page
from scrapers.base_scraper import BaseScraper


class BehanceScraper(BaseScraper):

    def __init__(self, username: str):
        super().__init__()
        self._username = username

    @property
    def url(self) -> str:
        return f"https://www.behance.net/{self._username}/followers"

    @property
    def name(self) -> str:
        return "Behance"

    def parse_page(self, page: Page):
        
        page.goto(self.url, wait_until="networkidle", timeout=90000)
        page.wait_for_selector('div.ScrollableModal-content-SvL', timeout=30000)

        collected_followers = set()
        max_followers = 10
        no_progress_rounds = 0
        max_no_progress = 8

        print(f"[{self.name}] Collecting up to {max_followers} followers...")

        while len(collected_followers) < max_followers and no_progress_rounds < max_no_progress:
            
            names = page.evaluate('''() => {
                return Array.from(document.querySelectorAll('h3.ProfileRow-displayName-ZZg a'))
                    .map(a => a.innerText.trim())
                    .filter(Boolean);
            }''')

            added = 0
            for name in names:
                if name not in collected_followers:
                    collected_followers.add(name)
                    added += 1
                    print(f"  → + {name} ({len(collected_followers)}/200)")

            if added == 0:
                no_progress_rounds += 1
            else:
                no_progress_rounds = 0

            if len(collected_followers) >= max_followers:
                break

            page.evaluate('''
                const modal = document.querySelector('div.ScrollableModal-scrollableTarget-IZX');
                if (modal) modal.scrollBy(0, modal.clientHeight * 3);
            ''')

            time.sleep(2.5)

        print(f"\n[{self.name}] FINAL → Collected {len(collected_followers)} followers")

        final_list = list(collected_followers)[:max_followers]

        self.data.append({
            "platform": "behance",
            "username": self._username,
            "url": self.url,
            "followers": final_list,
            "follower_count": len(final_list)
        })

        print(f"[{self.name}] SUCCESS → Saved {len(final_list)} followers of @{self._username}")
