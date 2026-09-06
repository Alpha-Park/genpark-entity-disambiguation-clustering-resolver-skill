"""
Example usage of Entity Disambiguation Clustering Resolver Skill.
"""

from client import EntityResolver


def main():
    print("=== Entity Disambiguation Clustering Resolver Demonstration ===")
    resolver = EntityResolver(similarity_threshold=0.82)

    mentions = [
        "OpenAI",
        "Open AI",
        "OpenAI Inc",
        "Anthropic",
        "Anthropic PBC",
        "Google DeepMind",
        "DeepMind",
        "Google Deep Mind",
        "Microsoft Corp",
        "Microsoft"
    ]

    print("Raw Entity Mentions (10 total):", mentions)
    clusters = resolver.resolve_entities(mentions)

    print("\nResolved Canonical Entities:")
    for c in clusters:
        print(f"  Canonical: '{c['canonical']}' (Size: {c['cluster_size']})")
        print(f"    Aliases: {c['aliases']}")


if __name__ == "__main__":
    main()
