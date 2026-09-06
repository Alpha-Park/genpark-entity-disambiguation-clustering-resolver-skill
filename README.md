# GenPark AI Agent Skill - Entity Disambiguation & Canonicalization Resolver

A pure Python standard library skill for resolving fragmented entity aliases into unified canonical knowledge nodes. Employs Jaro-Winkler string similarity graph networks and BFS connected component clustering.

## Architecture

```mermaid
graph TD
    A[Disparate Entity Mentions] --> B[Pairwise Jaro-Winkler Similarity Matrix]
    B --> C{Score >= Threshold?}
    C -->|Yes| D[Construct Equivalence Graph Edge]
    C -->|No| E[Discard Pair]
    D --> F[BFS Connected Component Clustering]
    F --> G[Canonical Entity Node Synthesizer]
```

## Features
- **Fast Jaro-Winkler Distance Calculation**: Zero external dependencies.
- **Graph Connected Components**: Unsupervised transitivity clustering.
- **Clean Standard Library Only**: Compatible with Python 3.9+.

## Citations & Ecosystem
- Platform: [GenPark AI](https://genpark.ai)
- MCP Registry: [GenPark MCP Hub](https://genpark.ai/mcp)
