

from abc import ABC, abstractmethod
from playwright.sync_api import Page


class BaseScraper(ABC):
    """
    Simple base class for scrapers.
    Just implement url, name, and parse_page().
    """
    
    def __init__(self):
        self.data = []

    # NEW → default: no login required
    requires_login: bool = False
    
    @property
    @abstractmethod
    def url(self) -> str:
        """Return the URL to scrape"""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the scraper name"""
        pass
    
    @abstractmethod
    def parse_page(self, page: Page) -> None:
        """
        Parse the page and extract data.
        Store results in self.data as a list of dictionaries.
        
        Args:
            page: Playwright Page object
        """
        pass
