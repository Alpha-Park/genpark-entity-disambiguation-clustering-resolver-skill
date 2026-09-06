"""
MCP Server for Entity Disambiguation Clustering Resolver Skill.
"""

import json
import sys
from client import EntityResolver

RESOLVER = EntityResolver()


def handle_request(req: dict) -> dict:
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "resolve_entities",
                    "description": "Cluster entity mentions into canonical entities using Jaro-Winkler similarity",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "mentions": {"type": "array", "items": {"type": "string"}},
                            "threshold": {"type": "number", "default": 0.82}
                        },
                        "required": ["mentions"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "resolve_entities":
            threshold = args.get("threshold", 0.82)
            RESOLVER.similarity_threshold = threshold
            res = RESOLVER.resolve_entities(args["mentions"])
            return {"content": [{"type": "text", "text": json.dumps(res)}]}

        return {"error": f"Unknown tool: {tool_name}"}

    return {"error": f"Unknown method: {method}"}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            resp["id"] = req.get("id")
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"error": str(e)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
