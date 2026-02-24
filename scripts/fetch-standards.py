#!/usr/bin/env python3
"""
Script to fetch latest W3C accessibility standards and convert them to JSON-LD format.

This script monitors W3C TR pages for WCAG, ARIA, ATAG, and UAAG standards
and generates updated JSON-LD documents when changes are detected.
"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup


def fetch_wcag_latest() -> Dict:
    """Fetch the latest WCAG specification from W3C."""
    url = "https://www.w3.org/TR/WCAG22/"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Check Last-Modified header
        last_modified = response.headers.get('Last-Modified', 'Unknown')
        etag = response.headers.get('ETag', 'Unknown')
        
        print(f"WCAG 2.2 - Last Modified: {last_modified}")
        print(f"WCAG 2.2 - ETag: {etag}")
        
        return {
            "url": url,
            "status": "available",
            "last_modified": last_modified,
            "etag": etag
        }
    except Exception as e:
        print(f"Error fetching WCAG: {e}")
        return {
            "url": url,
            "status": "error",
            "error": str(e)
        }


def fetch_aria_latest() -> Dict:
    """Fetch the latest ARIA specification from W3C."""
    url = "https://www.w3.org/TR/wai-aria-1.2/"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        last_modified = response.headers.get('Last-Modified', 'Unknown')
        etag = response.headers.get('ETag', 'Unknown')
        
        print(f"ARIA 1.2 - Last Modified: {last_modified}")
        print(f"ARIA 1.2 - ETag: {etag}")
        
        return {
            "url": url,
            "status": "available",
            "last_modified": last_modified,
            "etag": etag
        }
    except Exception as e:
        print(f"Error fetching ARIA: {e}")
        return {
            "url": url,
            "status": "error",
            "error": str(e)
        }


def fetch_atag_latest() -> Dict:
    """Fetch the latest ATAG specification from W3C."""
    url = "https://www.w3.org/TR/ATAG20/"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        last_modified = response.headers.get('Last-Modified', 'Unknown')
        etag = response.headers.get('ETag', 'Unknown')
        
        print(f"ATAG 2.0 - Last Modified: {last_modified}")
        print(f"ATAG 2.0 - ETag: {etag}")
        
        return {
            "url": url,
            "status": "available",
            "last_modified": last_modified,
            "etag": etag
        }
    except Exception as e:
        print(f"Error fetching ATAG: {e}")
        return {
            "url": url,
            "status": "error",
            "error": str(e)
        }


def fetch_uaag_latest() -> Dict:
    """Fetch the latest UAAG specification from W3C."""
    url = "https://www.w3.org/TR/UAAG20/"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        last_modified = response.headers.get('Last-Modified', 'Unknown')
        etag = response.headers.get('ETag', 'Unknown')
        
        print(f"UAAG 2.0 - Last Modified: {last_modified}")
        print(f"UAAG 2.0 - ETag: {etag}")
        
        return {
            "url": url,
            "status": "available",
            "last_modified": last_modified,
            "etag": etag
        }
    except Exception as e:
        print(f"Error fetching UAAG: {e}")
        return {
            "url": url,
            "status": "error",
            "error": str(e)
        }


def check_all_standards() -> Dict[str, Dict]:
    """Check all W3C accessibility standards."""
    print("Checking W3C Accessibility Standards...")
    print("=" * 60)
    
    standards = {
        "wcag": fetch_wcag_latest(),
        "aria": fetch_aria_latest(),
        "atag": fetch_atag_latest(),
        "uaag": fetch_uaag_latest()
    }
    
    return standards


def save_status_report(standards: Dict[str, Dict], output_file: str = "monitoring/standards-status.json"):
    """Save the status report to a JSON file."""
    report = {
        "checked_at": datetime.now().isoformat(),
        "standards": standards
    }
    
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nStatus report saved to: {output_file}")


def main():
    """Main function to check W3C standards."""
    standards = check_all_standards()
    
    # Create monitoring directory if it doesn't exist
    import os
    os.makedirs("monitoring", exist_ok=True)
    
    # Save status report
    save_status_report(standards)
    
    # Check if any standards have errors
    errors = [name for name, info in standards.items() if info.get("status") == "error"]
    
    if errors:
        print(f"\n⚠️  Errors detected for: {', '.join(errors)}")
        sys.exit(1)
    else:
        print("\n✅ All standards checked successfully")
        sys.exit(0)


if __name__ == "__main__":
    main()
