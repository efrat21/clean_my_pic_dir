import os
import mcp
import json

@mcp.tool()
def scan_folder(path: str) -> json[str]:
    """Scan a folder recursively and return all file paths."""
    results: json[str] = []
    for root, _, files in os.walk(path):
        for filename in files:
            results.append(os.path.join(root, filename))
    return results
