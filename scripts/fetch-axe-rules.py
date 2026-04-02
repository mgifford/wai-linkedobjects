#!/usr/bin/env python3
"""
Script to fetch latest axe-core rules from GitHub.

This script fetches the latest rule definitions from the axe-core repository
and generates an updated JSON-LD document.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
import requests


def fetch_axe_rules() -> dict:
    """Fetch axe-core rules from GitHub API."""
    print("Fetching axe-core rules...")
    
    # Get latest release info
    releases_url = "https://api.github.com/repos/dequelabs/axe-core/releases/latest"
    
    try:
        response = requests.get(releases_url, timeout=30)
        response.raise_for_status()
        release_data = response.json()
        
        version = release_data.get("tag_name", "unknown").replace("v", "")
        published_at = release_data.get("published_at", "unknown")
        
        print(f"Latest axe-core version: {version}")
        print(f"Published at: {published_at}")
        
        return {
            "status": "success",
            "version": version,
            "published_at": published_at,
            "url": "https://github.com/dequelabs/axe-core"
        }
        
    except Exception as e:
        print(f"Error fetching axe-core rules: {e}")
        return {
            "status": "error",
            "error": str(e)
        }


def save_status_report(axe_info: dict, output_file: str = "monitoring/axe-status.json") -> None:
    """Save the status report to a JSON file."""
    report = {
        "checked_at": datetime.now().isoformat(),
        "axe-core": axe_info
    }

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"Status report saved to: {output_file}")


def main():
    """Main function to check axe-core rules."""
    axe_info = fetch_axe_rules()
    
    # Save status report
    save_status_report(axe_info)
    
    if axe_info.get("status") == "error":
        print("\n⚠️  Error checking axe-core")
        sys.exit(1)
    else:
        print("\n✅ axe-core checked successfully")
        sys.exit(0)


if __name__ == "__main__":
    main()
