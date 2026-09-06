"""
Entity Disambiguation Clustering Resolver Skill Client
Pure Python Standard Library implementation of entity resolution and canonicalization.
Calculates Jaro-Winkler similarity between alias mentions, builds equivalence graphs,
and groups aliases into canonical clusters via connected components.
"""

from typing import List, Dict, Any, Set, Tuple


class EntityResolver:
    """
    Unsupervised entity disambiguation and resolution engine.
    """

    def __init__(self, similarity_threshold: float = 0.82):
        self.similarity_threshold = similarity_threshold

    @staticmethod
    def jaro_winkler(s1: str, s2: str, prefix_scale: float = 0.1) -> float:
        """Calculate Jaro-Winkler string similarity."""
        s1 = s1.lower().strip()
        s2 = s2.lower().strip()

        if s1 == s2:
            return 1.0

        len1, len2 = len(s1), len(s2)
        if len1 == 0 or len2 == 0:
            return 0.0

        max_dist = max(len1, len2) // 2 - 1
        s1_matches = [False] * len1
        s2_matches = [False] * len2

        matches = 0
        transpositions = 0

        for i in range(len1):
            start = max(0, i - max_dist)
            end = min(i + max_dist + 1, len2)
            for j in range(start, end):
                if s2_matches[j]:
                    continue
                if s1[i] == s2[j]:
                    s1_matches[i] = True
                    s2_matches[j] = True
                    matches += 1
                    break

        if matches == 0:
            return 0.0

        k = 0
        for i in range(len1):
            if not s1_matches[i]:
                continue
            while not s2_matches[k]:
                k += 1
            if s1[i] != s2[k]:
                transpositions += 1
            k += 1

        jaro = (
            (matches / len1) +
            (matches / len2) +
            ((matches - (transpositions / 2)) / matches)
        ) / 3.0

        # Prefix bonus
        prefix_len = 0
        for i in range(min(4, len1, len2)):
            if s1[i] == s2[i]:
                prefix_len += 1
            else:
                break

        return jaro + prefix_len * prefix_scale * (1.0 - jaro)

    def resolve_entities(self, mentions: List[str]) -> List[Dict[str, Any]]:
        """
        Cluster list of entity mentions into canonical groups.
        """
        unique_mentions = list(dict.fromkeys(m.strip() for m in mentions if m.strip()))
        n = len(unique_mentions)
        adjacency: Dict[int, Set[int]] = {i: set() for i in range(n)}

        for i in range(n):
            for j in range(i + 1, n):
                score = self.jaro_winkler(unique_mentions[i], unique_mentions[j])
                if score >= self.similarity_threshold:
                    adjacency[i].add(j)
                    adjacency[j].add(i)

        # Connected components via BFS
        visited = set()
        clusters = []

        for i in range(n):
            if i in visited:
                continue
            component = []
            queue = [i]
            visited.add(i)

            while queue:
                curr = queue.pop(0)
                component.append(curr)
                for neighbor in adjacency[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

            cluster_mentions = [unique_mentions[idx] for idx in component]
            # Pick canonical form: longest or most capitalized representation
            canonical = max(cluster_mentions, key=lambda x: (sum(1 for c in x if c.isupper()), len(x)))
            clusters.append({
                "canonical": canonical,
                "aliases": cluster_mentions,
                "cluster_size": len(cluster_mentions)
            })

        return sorted(clusters, key=lambda c: c["cluster_size"], reverse=True)
