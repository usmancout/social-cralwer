import time
from playwright.sync_api import Page
from abc import ABC, abstractmethod

from scrapers.base_scraper import BaseScraper
from models import social_model
from cross_platform_mapping import cross_platform_mapper


class FacebookScraper(BaseScraper):
    requires_login = True

    def __init__(self, username: str):
        super().__init__()
        self._username = username

    @property
    def follower_url(self) -> str:
        return f"https://web.facebook.com/{self._username}/followers"

    @property
    def following_url(self) -> str:
        return f"https://web.facebook.com/{self._username}/following"

    @property
    def base_url(self) -> str:
        return "https://web.facebook.com"

    @property
    def name(self) -> str:
        return "Facebook"

    def _extract_names(self, page: Page):
        selectors = [
            'a[href*="profile.php?id"] span[dir="auto"]',

        ]
        for selector in selectors:
            try:
                items = page.query_selector_all(selector)
                if items:
                    return [i.inner_text().strip() for i in items if i.inner_text()]
            except:
                pass
        return []

    def _collect_from_urls(self, page: Page, urls: list, label: str, max_items=10):
        for url in urls:
            try:
                print(f"[Facebook] Collecting {label} (max {max_items})...")
                page.goto(url, wait_until="networkidle", timeout=90000)
                time.sleep(3)

                collected = []
                seen = set()
                rounds_no_progress = 0

                while len(collected) < max_items and rounds_no_progress < 6:
                    names = self._extract_names(page)
                    added = 0
                    for n in names:
                        if n not in seen:
                            seen.add(n)
                            collected.append(n)
                            print(f" → + {n} ({len(collected)}/{max_items})")
                            added += 1
                            if len(collected) >= max_items:
                                break
                    if added == 0:
                        rounds_no_progress += 1
                    else:
                        rounds_no_progress = 0

                    if len(collected) >= max_items:
                        break

                    page.mouse.wheel(0, 2000)
                    time.sleep(2)

                if collected:
                    return collected[:max_items]

            except:
                continue

        print(f"[Facebook] Warning: No elements detected for {label}.")
        return []

    def parse_page(self, page: Page):

        followers = self._collect_from_urls(
            page,
            urls=[
                self.follower_url,
                f"https://web.facebook.com/{self._username}/friends",
                f"https://web.facebook.com/{self._username}/friends_all",
            ],
            label="followers",
            max_items=10
        )

        following = self._collect_from_urls(
            page,
            urls=[
                self.following_url,
                f"https://web.facebook.com/{self._username}/friends",
                f"https://web.facebook.com/{self._username}/friends_all",
            ],
            label="following",
            max_items=10
        )

        mutual = list(set(followers) & set(following))

        print(f"[Facebook] Mutual connections found: {len(mutual)}")

        card = social_model(
            m_weblink=[self.follower_url, self.following_url],
            m_content=f"Followers: {followers}\nFollowing: {following}\nMutual: {mutual}",
            m_content_type=["facebook_followers", "facebook_following", "facebook_mutual"],
            m_network="clearnet",
            m_platform="facebook",
            m_commenters=followers,
            m_mutual_usernames=mutual
        )

        self.data.append(card.model_dump())
        
        # Send card to cross-platform mapper
        cross_platform_mapper.add_card(card)
