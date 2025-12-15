"""
Cross-Platform Mapping Module
Collects and stores card instances from multiple scrapers,
then prints all collected cards at the end.
"""
from rapidfuzz import fuzz, process
from typing import List
from difflib import SequenceMatcher
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
        self._cards.append(card)
        print(f"[CrossPlatformMapper] Card added from platform: {card.m_platform}")

    def get_all_cards(self) -> List[social_model]:
        return self._cards

    def print_all_cards(self) -> None:
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
        self._cards = []
        print("[CrossPlatformMapper] All cards cleared.")

    # -----------------------------------------------------------------
    # 🔥 NEW FEATURE: Cross-Platform Following Username Comparison
    # -----------------------------------------------------------------


    def compare_following_across_platforms(self, threshold: float = 70):
        """
        Compares following lists of all platforms using rapidfuzz:
          - exact matches
          - fuzzy username matches (based on similarity score)
          - unique usernames on each platform

        Args:
            threshold: minimum similarity score (0-100) to consider a match
        """

        print("\n" + "=" * 60)
        print("CROSS-PLATFORM FOLLOWING USERNAME COMPARISON (RapidFuzz)")
        print("=" * 60)

        # Extract only cards with following lists
        platform_following = {
            card.m_platform: card.m_following
            for card in self._cards
            if card.m_following
        }

        if len(platform_following) < 2:
            print("Not enough platforms with following lists.")
            return

        platforms = list(platform_following.keys())

        for i in range(len(platforms)):
            for j in range(i + 1, len(platforms)):
                p1, p2 = platforms[i], platforms[j]
                list1 = platform_following[p1]
                list2 = platform_following[p2]

                print(f"\n>>> Comparing: {p1} vs {p2}")

                # Exact matches
                exact = set(list1) & set(list2)
                print(f"Exact Matches ({len(exact)}): {list(exact)}")

                # Fuzzy matches using rapidfuzz process.extract
                fuzzy_matches = []
                for u1 in list1:
                    matches = (process.extract(u1,list2,scorer=fuzz.ratio,score_cutoff=threshold))

                    for match_name, score, _ in matches:
                        if u1 != match_name:
                            fuzzy_matches.append((u1, match_name, round(score, 2)))

                print(f"Fuzzy Matches ({len(fuzzy_matches)}): {fuzzy_matches}")

                # Unique users
                unique_p1 = set(list1) - set(list2)
                unique_p2 = set(list2) - set(list1)
                print(f"Only on {p1}: {list(unique_p1)}")
                print(f"Only on {p2}: {list(unique_p2)}")

        print("\n" + "=" * 60 + "\n")


# Global instance for easy access
cross_platform_mapper = CrossPlatformMapper()
