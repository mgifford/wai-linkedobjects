#!/usr/bin/env python3
"""
Script to fetch latest W3C accessibility standards and convert them to JSON-LD format.

This script monitors W3C TR pages for WCAG, ARIA, ATAG, and UAAG standards
and generates updated JSON-LD documents when changes are detected.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
import requests
from bs4 import BeautifulSoup


def _fetch_standard(name: str, url: str) -> dict:
    """Fetch a W3C standard URL and return status metadata.

    Args:
        name: Human-readable label used in log output (e.g. "WCAG 2.2").
        url: The canonical URL of the W3C specification.

    Returns:
        A dict with keys ``url``, ``status``, ``last_modified``, and
        ``etag`` on success, or ``url``, ``status``, and ``error`` on
        failure.
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        last_modified = response.headers.get('Last-Modified', 'Unknown')
        etag = response.headers.get('ETag', 'Unknown')

        print(f"{name} - Last Modified: {last_modified}")
        print(f"{name} - ETag: {etag}")

        return {
            "url": url,
            "status": "available",
            "last_modified": last_modified,
            "etag": etag,
        }
    except requests.RequestException as e:
        print(f"Error fetching {name}: {e}")
        return {
            "url": url,
            "status": "error",
            "error": str(e),
        }


def fetch_wcag_latest() -> dict:
    """Fetch the latest WCAG specification from W3C."""
    return _fetch_standard("WCAG 2.2", "https://www.w3.org/TR/WCAG22/")


def fetch_aria_latest() -> dict:
    """Fetch the latest ARIA specification from W3C."""
    return _fetch_standard("ARIA 1.2", "https://www.w3.org/TR/wai-aria-1.2/")


def fetch_atag_latest() -> dict:
    """Fetch the latest ATAG specification from W3C."""
    return _fetch_standard("ATAG 2.0", "https://www.w3.org/TR/ATAG20/")


def fetch_uaag_latest() -> dict:
    """Fetch the latest UAAG specification from W3C."""
    return _fetch_standard("UAAG 2.0", "https://www.w3.org/TR/UAAG20/")


def check_all_standards() -> dict[str, dict]:
    """Check all W3C accessibility standards."""
    print("Checking W3C Accessibility Standards...")
    print("=" * 60)

    return {
        "wcag": fetch_wcag_latest(),
        "aria": fetch_aria_latest(),
        "atag": fetch_atag_latest(),
        "uaag": fetch_uaag_latest(),
    }


def save_status_report(
    standards: dict[str, dict],
    output_file: str = "monitoring/standards-status.json",
) -> None:
    """Save the status report to a JSON file."""
    report = {
        "checked_at": datetime.now().isoformat(),
        "standards": standards,
    }

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\nStatus report saved to: {output_file}")


def main() -> int:
    """Main function to check W3C standards."""
    standards = check_all_standards()

    save_status_report(standards)

    errors = [name for name, info in standards.items() if info.get("status") == "error"]

    if errors:
        print(f"\n⚠️  Errors detected for: {', '.join(errors)}")
        return 1

    print("\n✅ All standards checked successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
