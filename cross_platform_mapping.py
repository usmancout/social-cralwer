from typing import List, Tuple, Dict
from rapidfuzz import fuzz

from models import social_model


class CrossPlatformMapper:

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
        print("CROSS-PLATFORM MAPPING - ALL COLLECTED CARDS")

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

        print(f"\nTotal cards collected: {len(self._cards)}")

    def clear_cards(self) -> None:
        self._cards = []
        print("[CrossPlatformMapper] All cards cleared.")

    def compare_following_across_platforms(self, threshold: int = 70) -> None:
        print("CROSS-PLATFORM FOLLOWING COMPARISON (PAIRWISE)")

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

                exact = sorted(set(list1) & set(list2))
                print(f"Exact Matches ({len(exact)}): {exact}")

                similar: List[Tuple[str, str, float]] = []
                for u1 in list1:
                    for u2 in list2:
                        if u1 == u2:
                            continue
                        score = fuzz.ratio(u1.lower(), u2.lower())
                        if score >= threshold:
                            similar.append((u1, u2, score))

                print(
                    f"Similar Matches ({len(similar)}): "
                    f"{[(u1, u2, f'{s}%') for u1, u2, s in similar]}"
                )

                only_p1 = sorted(set(list1) - set(list2))
                only_p2 = sorted(set(list2) - set(list1))
                print(f"Only on {p1}: {only_p1}")
                print(f"Only on {p2}: {only_p2}")

    def group_following_across_all_platforms(self, threshold: int = 70) -> None:
        print("GLOBAL USERNAME IDENTITY GROUPING")

        users: List[Tuple[str, str]] = []
        for card in self._cards:
            if card.m_following:
                for username in card.m_following:
                    users.append((card.m_platform, username))

        if not users:
            print("No following data available.")
            print("=" * 60)
            return

        groups: List[List[Tuple[str, str]]] = []

        for platform, username in users:
            matched = False
            for group in groups:
                if any(fuzz.ratio(username, existing_username) >= threshold
                       for _, existing_username in group):
                    group.append((platform, username))
                    matched = True
                    break
            if not matched:
                groups.append([(platform, username)])

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

    def analyze_cross_platform_influence(self, threshold: int = 70) -> None:
        print("CROSS-PLATFORM INFLUENCE & NETWORK INTELLIGENCE")

        user_profiles: Dict[str, Dict] = {}

        for card in self._cards:
            platform = card.m_platform
            all_connections = []

            if card.m_followers:
                for user in card.m_followers:
                    all_connections.append((user, 'follower', platform))

            if card.m_following:
                for user in card.m_following:
                    all_connections.append((user, 'following', platform))

            if card.m_mutual_usernames:
                for user in card.m_mutual_usernames:
                    all_connections.append((user, 'mutual', platform))

            for username, conn_type, plat in all_connections:
                norm_username = username.lower().strip()
                matched_key = None

                for existing_key in user_profiles.keys():
                    if fuzz.ratio(norm_username, existing_key) >= threshold:
                        matched_key = existing_key
                        break

                if not matched_key:
                    matched_key = norm_username
                    user_profiles[matched_key] = {
                        'original_names': set(),
                        'platforms': set(),
                        'connection_types': set(),
                        'follower_count': 0,
                        'following_count': 0,
                        'mutual_count': 0,
                        'platform_details': {}
                    }

                profile = user_profiles[matched_key]
                profile['original_names'].add(username)
                profile['platforms'].add(plat)
                profile['connection_types'].add(conn_type)

                if conn_type == 'follower':
                    profile['follower_count'] += 1
                elif conn_type == 'following':
                    profile['following_count'] += 1
                elif conn_type == 'mutual':
                    profile['mutual_count'] += 1

                profile.setdefault('platform_details', {}).setdefault(plat, []).append(conn_type)

        if not user_profiles:
            print("No user data available for analysis.")
            print("=" * 60)
            return

        scored_users = []

        for username, profile in user_profiles.items():
            platform_diversity = len(profile['platforms'])
            connection_diversity = len(profile['connection_types'])

            network_score = (
                profile['follower_count'] * 1.5 +
                profile['mutual_count'] * 2.0 +
                profile['following_count'] * 0.5
            )

            influence_score = (
                platform_diversity * 10 +
                connection_diversity * 5 +
                network_score
            )

            scored_users.append({
                'username': username,
                'profile': profile,
                'score': influence_score
            })

        scored_users.sort(key=lambda x: x['score'], reverse=True)

        print("\n>>> TOP CROSS-PLATFORM INFLUENCERS")
        print("-" * 60)

        for i, user_data in enumerate(scored_users[:10], 1):
            profile = user_data['profile']
            print(f"\n{i}. Username Variations: {sorted(profile['original_names'])}")
            print(f"   Influence Score: {user_data['score']:.1f}")
            print(f"   Platforms: {sorted(profile['platforms'])}")
            print(f"   Connection Types: {sorted(profile['connection_types'])}")
            print(f"   Network Stats: {profile['follower_count']} followers, "
                  f"{profile['following_count']} following, "
                  f"{profile['mutual_count']} mutual")

            print("   Platform Breakdown:")
            for plat, types in sorted(profile['platform_details'].items()):
                print(f"      {plat}: {', '.join(sorted(set(types)))}")

        print("\n\n>>> CROSS-PLATFORM BRIDGE USERS (Multi-Platform Connectors)")
        print("-" * 60)

        bridge_users = [u for u in scored_users if len(u['profile']['platforms']) >= 2]

        for user_data in bridge_users[:15]:
            profile = user_data['profile']
            platforms_str = " ↔ ".join(sorted(profile['platforms']))
            names_str = " / ".join(sorted(profile['original_names']))
            print(f"  • {names_str}")
            print(f"    Bridges: {platforms_str}")
            print(f"    Connection Types: {', '.join(sorted(profile['connection_types']))}")

        print("\n\n>>> NETWORK STATISTICS")
        print("-" * 60)

        total_users = len(user_profiles)
        multi_platform = len([u for u in user_profiles.values() if len(u['platforms']) > 1])
        avg_platforms = sum(len(u['platforms']) for u in user_profiles.values()) / total_users

        print(f"Total Unique Users: {total_users}")
        print(f"Multi-Platform Users: {multi_platform} ({multi_platform/total_users*100:.1f}%)")
        print(f"Average Platforms per User: {avg_platforms:.2f}")

        conn_type_dist = {}
        for profile in user_profiles.values():
            for conn_type in profile['connection_types']:
                conn_type_dist[conn_type] = conn_type_dist.get(conn_type, 0) + 1

        print("\nConnection Type Distribution:")
        for conn_type, count in sorted(conn_type_dist.items(), key=lambda x: x[1], reverse=True):
            print(f"  {conn_type}: {count} users")

        print("\n" + "=" * 60)


cross_platform_mapper = CrossPlatformMapper()
