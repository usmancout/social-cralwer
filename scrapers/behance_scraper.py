import time
from playwright.sync_api import Page
from scrapers.base_scraper import BaseScraper
from models import social_model
from cross_platform_mapping import cross_platform_mapper


class BehanceScraper(BaseScraper):

    def __init__(self, username: str):
        super().__init__()
        self._username = username

    @property
    def base_url(self) -> str:
        return f"https://www.behance.net"

    @property
    def follower_url(self) -> str:
        return f"https://www.behance.net/{self._username}/followers"

    @property
    def following_url(self) -> str:
        return f"https://www.behance.net/{self._username}/following"

    @property
    def name(self) -> str:
        return "Behance"

    def _collect_names(self, page: Page, url: str, label: str, max_items=10):
        """
        Shared logic for collecting followers/following list.
        """
        page.goto(url, wait_until="networkidle", timeout=90000)
        page.wait_for_selector('div.ScrollableModal-content-SvL', timeout=30000)

        collected = set()
        no_progress_rounds = 0
        max_no_progress = 8

        print(f"[{self.name}] Collecting {label} (max {max_items})...")

        while len(collected) < max_items and no_progress_rounds < max_no_progress:

            names = page.evaluate('''
                () => Array.from(document.querySelectorAll('h3.ProfileRow-displayName-ZZg a'))
                           .map(a => a.innerText.trim())
                           .filter(Boolean)
            ''')

            added = 0
            for n in names:
                if n not in collected:
                    collected.add(n)
                    added += 1
                    print(f"  → + {n} ({len(collected)}/{max_items})")

            if added == 0:
                no_progress_rounds += 1
            else:
                no_progress_rounds = 0

            if len(collected) >= max_items:
                break

            page.evaluate('''
                const modal = document.querySelector('div.ScrollableModal-scrollableTarget-IZX');
                if (modal) modal.scrollBy(0, modal.clientHeight * 3);
            ''')

            time.sleep(2.5)

        return list(collected)[:max_items]

    def parse_page(self, page: Page):

        # Collect followers
        followers = self._collect_names(
            page,
            url=self.follower_url,
            label="followers"
        )

        # Collect following
        following = self._collect_names(
            page,
            url=self.following_url,
            label="following"
        )

        # Find mutual usernames
        mutual_usernames = list(set(followers) & set(following))

        print(f"[{self.name}] Mutual connections: {mutual_usernames}")

        # Build model
        card = social_model(
            m_weblink=[self.follower_url, self.following_url],
            m_content=(
                f"Followers of {self._username}: {', '.join(followers)} | "
                f"Following: {', '.join(following)} | "
                f"Mutual: {', '.join(mutual_usernames)}"
            ),
            m_content_type=["behance_followers", "behance_following", "behance_mutual"],
            m_network="clearnet",
            m_platform="behance",

            m_followers=followers,
            m_following=following,
            m_mutual_usernames=mutual_usernames  # <-- added
        )

        print(card)
        self.data.append(card.model_dump())
        
        # Send card to cross-platform mapper
        cross_platform_mapper.add_card(card)

