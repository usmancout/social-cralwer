from playwright.sync_api import Page
from scrapers.base_scraper import BaseScraper
from models import social_model
from cross_platform_mapping import cross_platform_mapper


class vimeo(BaseScraper):

    requires_login = False

    def __init__(self, username: str):
        super().__init__()
        self._username = username

    @property
    def base_url(self) -> str:
        return f"https://vimeo.com/{self._username}"

    @property
    def url(self) -> str:
        return f"https://vimeo.com/{self._username}"

    @property
    def name(self) -> str:
        return "Vimeo"

    def parse_page(self, page: Page):

        base_url = "https://www.vimeo.com"
        username = page.locator("div.sc-aa85dd4c-2 span div.sc-aa85dd4c-7").first.inner_text().strip()
        print(f"{username}: {page.url}")

        followers_anchor = page.locator("a[href*='following/followers']")

        followers_text = followers_anchor.inner_text().strip()
        followers_link = followers_anchor.get_attribute("href")
        print(f"{followers_text}: {followers_link}")

        following_anchor = page.locator("a[href$='/following']")

        following_text = following_anchor.inner_text().strip()
        following_link = following_anchor.get_attribute("href")
        print(f"{following_text}: {following_link}")

        followers_url = followers_link
        following_url = following_link

        page.goto(followers_url)

        followers_data = []

        for page_number in range(1, 20):

            blocks = page.query_selector_all("div.data")

            for b in blocks:
                title_el = b.query_selector("p.title")
                title = title_el.inner_text().strip() if title_el else ""

                followers_data.append(title)

            next_btn = page.query_selector("li.pagination_next a")

            if next_btn:
                next_href = next_btn.get_attribute("href")
                if not next_href:
                    break

                next_page_url = base_url + next_href
                page.goto(next_page_url)

            else:
                break

        print(followers_data)

        page.goto(following_url)

        following_data = []

        for page_number in range(1, 20):

            blocks = page.query_selector_all("div.data")

            for b in blocks:
                title_el = b.query_selector("p.title")
                title = title_el.inner_text().strip() if title_el else ""

                following_data.append(title)

            next_btn = page.query_selector("li.pagination_next a")

            if next_btn:
                next_href = next_btn.get_attribute("href")
                if not next_href:
                    break

                next_page_url = base_url + next_href
                page.goto(next_page_url)

            else:
                break

        print(following_data)

        # Build model and send to cross-platform mapper
        mutual = list(set(followers_data) & set(following_data))
        
        card = social_model(
            m_weblink=[followers_url, following_url],
            m_content=f"Followers: {followers_data}\nFollowing: {following_data}\nMutual: {mutual}",
            m_content_type=["vimeo_followers", "vimeo_following", "vimeo_mutual"],
            m_network="clearnet",
            m_platform="vimeo",
            m_followers=followers_data,
            m_following=following_data,
            m_mutual_usernames=mutual
        )

        print(card)
        self.data.append(card.model_dump())
        
        # Send card to cross-platform mapper
        cross_platform_mapper.add_card(card)
