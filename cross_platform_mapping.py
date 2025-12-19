"""
Cross-Platform Mapping Module
Collects and stores card instances from multiple scrapers,
then prints all collected cards at the end.
"""

from typing import List, Tuple
from rapidfuzz import fuzz

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
    # Cross-Platform Following Username Comparison (Pairwise)
    # -----------------------------------------------------------------
    def compare_following_across_platforms(self, threshold: int = 70) -> None:
        """
        Performs pairwise comparison of 'following' lists between all platforms.
        Uses RapidFuzz with extractOne for clean, type-safe fuzzy matching.
        """
        print("\n" + "=" * 60)
        print("CROSS-PLATFORM FOLLOWING COMPARISON (PAIRWISE)")
        print("=" * 60)

        # Collect unique following lists per platform
        platform_following = {
            card.m_platform: list(set(card.m_following))
            for card in self._cards
            if card.m_following
        }

        if len(platform_following) < 2:
            print("Not enough platforms with following data.")
            return

        platforms = list(platform_following.keys())

        for i in range(len(platforms)):
            for j in range(i + 1, len(platforms)):
                p1, p2 = platforms[i], platforms[j]
                list1 = platform_following[p1]
                list2 = platform_following[p2]

                print(f"\n>>> {p1}  VS  {p2}")

                # Exact matches
                exact = sorted(set(list1) & set(list2))
                print(f"Exact Matches ({len(exact)}): {exact}")

                # Similar matches (case-insensitive, partial)
                similar: List[Tuple[str, str,float]] = []
                for u1 in list1:
                    for u2 in list2:
                        # Skip if already an exact match
                        if u1 == u2:
                            continue
                        # Check similarity using direct ratio comparison
                        score = fuzz.ratio(u1.lower(), u2.lower())
                        if score >= threshold:
                            similar.append((u1, u2,score))

                print(
                    f"Similar Matches ({len(similar)}): "
                    f"{[(u1, u2, f'{s}%') for u1, u2, s in similar]}"
                )

                # Unique to each platform
                only_p1 = sorted(set(list1) - set(list2))
                only_p2 = sorted(set(list2) - set(list1))
                print(f"Only on {p1}: {only_p1}")
                print(f"Only on {p2}: {only_p2}")

        print("\n" + "=" * 60)

    # -----------------------------------------------------------------
    # Global multi-platform identity grouping
    # -----------------------------------------------------------------
    def group_following_across_all_platforms(self, threshold: int = 70) -> None:
        """
        Groups similar usernames across ALL platforms into identity clusters.
        Uses simple pairwise fuzz.ratio (direct and type-safe).
        """
        print("\n" + "=" * 60)
        print("GLOBAL USERNAME IDENTITY GROUPING")
        print("=" * 60)

        # Collect all (platform, username) pairs
        users: List[Tuple[str, str]] = []
        for card in self._cards:
            if card.m_following:
                for username in card.m_following:
                    users.append((card.m_platform, username))

        if not users:
            print("No following data available.")
            print("=" * 60)
            return

        # Greedy clustering: group usernames with similarity >= threshold
        groups: List[List[Tuple[str, str]]] = []

        for platform, username in users:
            matched = False
            for group in groups:
                # Check against any existing member in the group
                if any(fuzz.ratio(username, existing_username) >= threshold
                       for _, existing_username in group):
                    group.append((platform, username))
                    matched = True
                    break
            if not matched:
                groups.append([(platform, username)])

        # Print only groups with cross-platform matches
        meaningful_groups = [g for g in groups if len(g) > 1]
        if not meaningful_groups:
            print("No cross-platform identities found above threshold.")
        else:
            for idx, group in enumerate(meaningful_groups, 1):
                print(f"\nIdentity Group {idx}:")
                for platform, username in sorted(group):
                    scores = [
                        fuzz.ratio(username, other)
                        for _, other in group
                        if other != username
                    ]
                    confidence = max(scores) if scores else 100
                    print(f"  {platform}: {username} ({confidence}%)")

        print("\n" + "=" * 60)


# Global singleton instance
cross_platform_mapper = CrossPlatformMapper()