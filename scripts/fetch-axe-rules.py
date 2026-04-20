#!/usr/bin/env python3
"""
Script to fetch latest axe-core rules from GitHub.

This script fetches the latest rule definitions from the axe-core repository
and generates an updated JSON-LD document.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
import requests


RELEASES_URL = (
    "https://api.github.com/repos/dequelabs/axe-core/releases/latest"
)


def fetch_axe_rules() -> dict:
    """Fetch axe-core rules from GitHub API."""
    print("Fetching axe-core rules...")

    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.get(RELEASES_URL, headers=headers, timeout=30)
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

    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 403:
            print(
                f"GitHub API rate limit exceeded; skipping axe-core check: {e}"
            )
            return {
                "status": "rate_limited",
                "error": str(e),
                "url": "https://github.com/dequelabs/axe-core",
            }
        print(f"HTTP error fetching axe-core rules: {e}")
        return {
            "status": "error",
            "error": str(e),
        }

    except requests.RequestException as e:
        print(f"Error fetching axe-core rules: {e}")
        return {
            "status": "error",
            "error": str(e),
        }


def save_status_report(
    axe_info: dict,
    output_file: str = "monitoring/axe-status.json",
) -> None:
    """Save the status report to a JSON file."""
    report = {
        "checked_at": datetime.now().isoformat(),
        "axe-core": axe_info
    }

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"Status report saved to: {output_file}")


def main() -> int:
    """Main function to check axe-core rules."""
    axe_info = fetch_axe_rules()

    # Save status report
    save_status_report(axe_info)

    if axe_info.get("status") == "error":
        print("\n⚠️  Error checking axe-core")
        return 1
    elif axe_info.get("status") == "rate_limited":
        print("\n⚠️  GitHub API rate limit reached; axe-core check skipped")
        return 0
    else:
        print("\n✅ axe-core checked successfully")
        return 0


if __name__ == "__main__":
    sys.exit(main())
