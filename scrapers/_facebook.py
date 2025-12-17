import time
from playwright.sync_api import Page

from scrapers.base_scraper import BaseScraper
from models import social_model
from cross_platform_mapping import cross_platform_mapper


class FacebookScraper(BaseScraper):
    requires_login = True

    def __init__(self, username: str):
        super().__init__()
        self._username = username

    @property
    def seed_url(self) -> str:
        return f"https://www.facebook.com/{self._username}=friends"

    @property
    def base_url(self) -> str:
        return "https://www.facebook.com"

    @property
    def name(self) -> str:
        return "Facebook"

    def _extract_names(self, page: Page):
        selectors = [
            'a[href*="profile.php?id"] span[dir="auto"]',
            'a[href^="/"] span[dir="auto"]'
        ]

        for selector in selectors:
            try:
                items = page.query_selector_all(selector)
                if items:
                    return [i.inner_text().strip() for i in items if i.inner_text()]
            except:
                pass

        return []

    def _collect_friends(self, page: Page, max_items=50):
        print(f"[Facebook] Collecting friends (max {max_items})...")
        page.goto(self.seed_url, wait_until="networkidle", timeout=90000)
        time.sleep(3)

        collected = []
        seen = set()
        rounds_no_progress = 0

        while len(collected) < max_items and rounds_no_progress < 6:
            names = self._extract_names(page)
            added = 0

            for name in names:
                if name not in seen:
                    seen.add(name)
                    collected.append(name)
                    print(f" → + {name} ({len(collected)}/{max_items})")
                    added += 1

                if len(collected) >= max_items:
                    break

            if added == 0:
                rounds_no_progress += 1
            else:
                rounds_no_progress = 0

            page.mouse.wheel(0, 2500)
            time.sleep(2)

        return collected[:max_items]

    def parse_page(self, page: Page):
        friends = self._collect_friends(page, max_items=50)

        print(f"[Facebook] Friends collected: {len(friends)}")

        card = social_model(
            m_weblink=[self.seed_url],
            m_content=f"Friends: {friends}",
            m_content_type=["facebook_friends"],
            m_network="clearnet",
            m_platform="facebook",
            m_commenters=friends,
            m_mutual_usernames=friends
        )

        self.data.append(card.model_dump())
        cross_platform_mapper.add_card(card)
