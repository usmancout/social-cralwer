"""
Cross-Platform Mapping Module
Collects and stores card instances from multiple scrapers,
then prints all collected cards at the end.
"""

from typing import List
from models import social_model


class CrossPlatformMapper:
    """
    Singleton-like collector that stores card instances from multiple scrapers.
    """
    _instance = None
    _cards: List[social_model] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._cards = []
        return cls._instance

    def add_card(self, card: social_model) -> None:
        """
        Add a card instance to the collection.
        
        Args:
            card: A social_model instance from a scraper
        """
        self._cards.append(card)
        print(f"[CrossPlatformMapper] Card added from platform: {card.m_platform}")

    def get_all_cards(self) -> List[social_model]:
        """
        Get all collected cards.
        
        Returns:
            List of all social_model instances
        """
        return self._cards

    def print_all_cards(self) -> None:
        """
        Print all collected cards in a formatted way.
        """
        print("\n" + "=" * 60)
        print("CROSS-PLATFORM MAPPING - ALL COLLECTED CARDS")
        print("=" * 60)
        
        if not self._cards:
            print("No cards collected.")
            return

        for i, card in enumerate(self._cards, 1):
            print(f"\n--- Card {i} ---")
            print(f"Platform: {card.m_platform}")
            print(f"Network: {card.m_network}")
            print(f"Web Links: {card.m_weblink}")
            print(f"Content Type: {card.m_content_type}")
            print(f"Content: {card.m_content}")
            
            if card.m_followers:
                print(f"Followers ({len(card.m_followers)}): {card.m_followers}")
            if card.m_following:
                print(f"Following ({len(card.m_following)}): {card.m_following}")
            if card.m_mutual_usernames:
                print(f"Mutual Connections ({len(card.m_mutual_usernames)}): {card.m_mutual_usernames}")
            if card.m_commenters:
                print(f"Commenters ({len(card.m_commenters)}): {card.m_commenters}")
            if card.m_post_likes:
                print(f"Post Likes: {card.m_post_likes}")
            if card.m_post_comments:
                print(f"Post Comments: {card.m_post_comments}")
            if card.m_post_views:
                print(f"Post Views: {card.m_post_views}")
            if card.m_views:
                print(f"Views: {card.m_views}")
            
            print("-" * 40)

        print(f"\nTotal cards collected: {len(self._cards)}")
        print("=" * 60 + "\n")

    def clear_cards(self) -> None:
        """
        Clear all collected cards.
        """
        self._cards = []
        print("[CrossPlatformMapper] All cards cleared.")


# Global instance for easy access
cross_platform_mapper = CrossPlatformMapper()
