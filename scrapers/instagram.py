from playwright.sync_api import Page
from scrapers.base_scraper import BaseScraper
from models import social_model
from cross_platform_mapping import cross_platform_mapper


class instagram(BaseScraper):

    requires_login = True

    def __init__(self, username: str):
        super().__init__()
        self._username = username

    @property
    def url(self) -> str:
        return f"https://www.instagram.com/{self._username}"

    @property
    def name(self) -> str:
        return "Instagram"

    def parse_page(self, page: Page):

        page.wait_for_selector("header")

        loc = page.locator("header h2, header span._ap3a")
        username = loc.first.inner_text() if loc.count() > 0 else ""
        print(username)

        loc = page.locator("header section h1, header section span[dir='auto']")
        real_name = loc.first.inner_text() if loc.count() > 0 else ""
        print(real_name)

        posts = page.locator("header section span span span").first
        total_posts = posts.inner_text() if posts.count() > 0 else ""
        print(total_posts)

        loc = page.locator("a[href$='/followers/'] span")
        followers = loc.nth(1).inner_text() if loc.count() > 1 else ""
        print(followers)

        loc = page.locator("a[href$='/following/'] span")
        following = loc.nth(1).inner_text() if loc.count() > 1 else ""
        print(following)

        bio = page.locator("header section span._ap3a._aaco._aacu._aacx._aad7._aade").first
        bio_text = bio.inner_text() if bio.count() > 0 else ""
        print("bio:", bio_text)

        page.click("a[href$='/following/']")
        page.wait_for_selector("div[role='dialog'] a.notranslate")

        loc = page.locator("div[role='dialog'] a.notranslate").first
        box = loc.bounding_box()
        page.mouse.move(box["x"] + box["width"] + 20, box["y"] + 10)

        for _ in range(5):
            page.mouse.wheel(0, 1500)
            page.wait_for_timeout(2000)

        loc = page.locator("div[role='dialog'] a.notranslate")
        following_user = loc.all_inner_texts()
        print(len(following_user), following_user)

        page.goto(self.url)
        page.click("a[href$='/followers/']")
        page.wait_for_selector("div[role='dialog'] a.notranslate")

        loc = page.locator("div[role='dialog'] a.notranslate").first
        box = loc.bounding_box()
        page.mouse.move(box["x"] + box["width"] + 20, box["y"] + 10)

        for _ in range(5):
            page.mouse.wheel(0, 1500)
            page.wait_for_timeout(2000)

        loc = page.locator("div[role='dialog'] a.notranslate")
        followers_user = loc.all_inner_texts()
        print(len(followers_user), followers_user)

        # Build model and send to cross-platform mapper
        mutual = list(set(followers_user) & set(following_user))
        
        card = social_model(
            m_weblink=[f"{self.url}/followers/", f"{self.url}/following/"],
            m_content=f"Followers: {followers_user}\nFollowing: {following_user}\nMutual: {mutual}",
            m_content_type=["instagram_followers", "instagram_following", "instagram_mutual"],
            m_network="clearnet",
            m_platform="instagram",
            m_followers=followers_user,
            m_following=following_user,
            m_mutual_usernames=mutual
        )

        print(card)
        self.data.append(card.model_dump())
        
        # Send card to cross-platform mapper
        cross_platform_mapper.add_card(card)

