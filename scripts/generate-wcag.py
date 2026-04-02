#!/usr/bin/env python3
"""
Generator script for WCAG JSON-LD files.

This script generates complete WCAG JSON-LD files with all success criteria
inline, using a comprehensive reference dataset that is faithful to the W3C standards.

The script can generate:
- WCAG 2.2 (78 success criteria)
- WCAG 2.1 (can be extended in the future)
"""

import json
import sys
from pathlib import Path
from datetime import datetime


# Complete WCAG 2.2 Success Criteria Reference
# This comprehensive list is based on the official W3C WCAG 2.2 Recommendation
# https://www.w3.org/TR/WCAG22/
WCAG_22_SUCCESS_CRITERIA = [
    # Principle 1: Perceivable
    # Guideline 1.1: Text Alternatives
    {"id": "1.1.1", "name": "Non-text Content", "level": "A", "guideline": "1.1"},
    
    # Guideline 1.2: Time-based Media
    {"id": "1.2.1", "name": "Audio-only and Video-only (Prerecorded)", "level": "A", "guideline": "1.2"},
    {"id": "1.2.2", "name": "Captions (Prerecorded)", "level": "A", "guideline": "1.2"},
    {"id": "1.2.3", "name": "Audio Description or Media Alternative (Prerecorded)", "level": "A", "guideline": "1.2"},
    {"id": "1.2.4", "name": "Captions (Live)", "level": "AA", "guideline": "1.2"},
    {"id": "1.2.5", "name": "Audio Description (Prerecorded)", "level": "AA", "guideline": "1.2"},
    {"id": "1.2.6", "name": "Sign Language (Prerecorded)", "level": "AAA", "guideline": "1.2"},
    {"id": "1.2.7", "name": "Extended Audio Description (Prerecorded)", "level": "AAA", "guideline": "1.2"},
    {"id": "1.2.8", "name": "Media Alternative (Prerecorded)", "level": "AAA", "guideline": "1.2"},
    {"id": "1.2.9", "name": "Audio-only (Live)", "level": "AAA", "guideline": "1.2"},
    
    # Guideline 1.3: Adaptable
    {"id": "1.3.1", "name": "Info and Relationships", "level": "A", "guideline": "1.3"},
    {"id": "1.3.2", "name": "Meaningful Sequence", "level": "A", "guideline": "1.3"},
    {"id": "1.3.3", "name": "Sensory Characteristics", "level": "A", "guideline": "1.3"},
    {"id": "1.3.4", "name": "Orientation", "level": "AA", "guideline": "1.3"},
    {"id": "1.3.5", "name": "Identify Input Purpose", "level": "AA", "guideline": "1.3"},
    {"id": "1.3.6", "name": "Identify Purpose", "level": "AAA", "guideline": "1.3"},
    
    # Guideline 1.4: Distinguishable
    {"id": "1.4.1", "name": "Use of Color", "level": "A", "guideline": "1.4"},
    {"id": "1.4.2", "name": "Audio Control", "level": "A", "guideline": "1.4"},
    {"id": "1.4.3", "name": "Contrast (Minimum)", "level": "AA", "guideline": "1.4"},
    {"id": "1.4.4", "name": "Resize Text", "level": "AA", "guideline": "1.4"},
    {"id": "1.4.5", "name": "Images of Text", "level": "AA", "guideline": "1.4"},
    {"id": "1.4.6", "name": "Contrast (Enhanced)", "level": "AAA", "guideline": "1.4"},
    {"id": "1.4.7", "name": "Low or No Background Audio", "level": "AAA", "guideline": "1.4"},
    {"id": "1.4.8", "name": "Visual Presentation", "level": "AAA", "guideline": "1.4"},
    {"id": "1.4.9", "name": "Images of Text (No Exception)", "level": "AAA", "guideline": "1.4"},
    {"id": "1.4.10", "name": "Reflow", "level": "AA", "guideline": "1.4"},
    {"id": "1.4.11", "name": "Non-text Contrast", "level": "AA", "guideline": "1.4"},
    {"id": "1.4.12", "name": "Text Spacing", "level": "AA", "guideline": "1.4"},
    {"id": "1.4.13", "name": "Content on Hover or Focus", "level": "AA", "guideline": "1.4"},
    
    # Principle 2: Operable
    # Guideline 2.1: Keyboard Accessible
    {"id": "2.1.1", "name": "Keyboard", "level": "A", "guideline": "2.1"},
    {"id": "2.1.2", "name": "No Keyboard Trap", "level": "A", "guideline": "2.1"},
    {"id": "2.1.3", "name": "Keyboard (No Exception)", "level": "AAA", "guideline": "2.1"},
    {"id": "2.1.4", "name": "Character Key Shortcuts", "level": "A", "guideline": "2.1"},
    
    # Guideline 2.2: Enough Time
    {"id": "2.2.1", "name": "Timing Adjustable", "level": "A", "guideline": "2.2"},
    {"id": "2.2.2", "name": "Pause, Stop, Hide", "level": "A", "guideline": "2.2"},
    {"id": "2.2.3", "name": "No Timing", "level": "AAA", "guideline": "2.2"},
    {"id": "2.2.4", "name": "Interruptions", "level": "AAA", "guideline": "2.2"},
    {"id": "2.2.5", "name": "Re-authenticating", "level": "AAA", "guideline": "2.2"},
    {"id": "2.2.6", "name": "Timeouts", "level": "AAA", "guideline": "2.2"},
    
    # Guideline 2.3: Seizures and Physical Reactions
    {"id": "2.3.1", "name": "Three Flashes or Below Threshold", "level": "A", "guideline": "2.3"},
    {"id": "2.3.2", "name": "Three Flashes", "level": "AAA", "guideline": "2.3"},
    {"id": "2.3.3", "name": "Animation from Interactions", "level": "AAA", "guideline": "2.3"},
    
    # Guideline 2.4: Navigable
    {"id": "2.4.1", "name": "Bypass Blocks", "level": "A", "guideline": "2.4"},
    {"id": "2.4.2", "name": "Page Titled", "level": "A", "guideline": "2.4"},
    {"id": "2.4.3", "name": "Focus Order", "level": "A", "guideline": "2.4"},
    {"id": "2.4.4", "name": "Link Purpose (In Context)", "level": "A", "guideline": "2.4"},
    {"id": "2.4.5", "name": "Multiple Ways", "level": "AA", "guideline": "2.4"},
    {"id": "2.4.6", "name": "Headings and Labels", "level": "AA", "guideline": "2.4"},
    {"id": "2.4.7", "name": "Focus Visible", "level": "AA", "guideline": "2.4"},
    {"id": "2.4.8", "name": "Location", "level": "AAA", "guideline": "2.4"},
    {"id": "2.4.9", "name": "Link Purpose (Link Only)", "level": "AAA", "guideline": "2.4"},
    {"id": "2.4.10", "name": "Section Headings", "level": "AAA", "guideline": "2.4"},
    {"id": "2.4.11", "name": "Focus Not Obscured (Minimum)", "level": "AA", "guideline": "2.4"},  # New in 2.2
    {"id": "2.4.12", "name": "Focus Not Obscured (Enhanced)", "level": "AAA", "guideline": "2.4"},  # New in 2.2
    {"id": "2.4.13", "name": "Focus Appearance", "level": "AAA", "guideline": "2.4"},  # New in 2.2
    
    # Guideline 2.5: Input Modalities
    {"id": "2.5.1", "name": "Pointer Gestures", "level": "A", "guideline": "2.5"},
    {"id": "2.5.2", "name": "Pointer Cancellation", "level": "A", "guideline": "2.5"},
    {"id": "2.5.3", "name": "Label in Name", "level": "A", "guideline": "2.5"},
    {"id": "2.5.4", "name": "Motion Actuation", "level": "A", "guideline": "2.5"},
    {"id": "2.5.5", "name": "Target Size (Enhanced)", "level": "AAA", "guideline": "2.5"},
    {"id": "2.5.6", "name": "Concurrent Input Mechanisms", "level": "AAA", "guideline": "2.5"},
    {"id": "2.5.7", "name": "Dragging Movements", "level": "AA", "guideline": "2.5"},  # New in 2.2
    {"id": "2.5.8", "name": "Target Size (Minimum)", "level": "AA", "guideline": "2.5"},  # New in 2.2
    
    # Principle 3: Understandable
    # Guideline 3.1: Readable
    {"id": "3.1.1", "name": "Language of Page", "level": "A", "guideline": "3.1"},
    {"id": "3.1.2", "name": "Language of Parts", "level": "AA", "guideline": "3.1"},
    {"id": "3.1.3", "name": "Unusual Words", "level": "AAA", "guideline": "3.1"},
    {"id": "3.1.4", "name": "Abbreviations", "level": "AAA", "guideline": "3.1"},
    {"id": "3.1.5", "name": "Reading Level", "level": "AAA", "guideline": "3.1"},
    {"id": "3.1.6", "name": "Pronunciation", "level": "AAA", "guideline": "3.1"},
    
    # Guideline 3.2: Predictable
    {"id": "3.2.1", "name": "On Focus", "level": "A", "guideline": "3.2"},
    {"id": "3.2.2", "name": "On Input", "level": "A", "guideline": "3.2"},
    {"id": "3.2.3", "name": "Consistent Navigation", "level": "AA", "guideline": "3.2"},
    {"id": "3.2.4", "name": "Consistent Identification", "level": "AA", "guideline": "3.2"},
    {"id": "3.2.5", "name": "Change on Request", "level": "AAA", "guideline": "3.2"},
    {"id": "3.2.6", "name": "Consistent Help", "level": "A", "guideline": "3.2"},  # New in 2.2
    
    # Guideline 3.3: Input Assistance
    {"id": "3.3.1", "name": "Error Identification", "level": "A", "guideline": "3.3"},
    {"id": "3.3.2", "name": "Labels or Instructions", "level": "A", "guideline": "3.3"},
    {"id": "3.3.3", "name": "Error Suggestion", "level": "AA", "guideline": "3.3"},
    {"id": "3.3.4", "name": "Error Prevention (Legal, Financial, Data)", "level": "AA", "guideline": "3.3"},
    {"id": "3.3.5", "name": "Help", "level": "AAA", "guideline": "3.3"},
    {"id": "3.3.6", "name": "Error Prevention (All)", "level": "AAA", "guideline": "3.3"},
    {"id": "3.3.7", "name": "Redundant Entry", "level": "A", "guideline": "3.3"},  # New in 2.2
    {"id": "3.3.8", "name": "Accessible Authentication (Minimum)", "level": "AA", "guideline": "3.3"},  # New in 2.2
    {"id": "3.3.9", "name": "Accessible Authentication (Enhanced)", "level": "AAA", "guideline": "3.3"},  # New in 2.2
    
    # Principle 4: Robust
    # Guideline 4.1: Compatible
    {"id": "4.1.2", "name": "Name, Role, Value", "level": "A", "guideline": "4.1"},
    {"id": "4.1.3", "name": "Status Messages", "level": "AA", "guideline": "4.1"},  # This was missing!
]


# Guideline structure for WCAG 2.2
WCAG_22_GUIDELINES = {
    "1.1": {
        "name": "Text Alternatives",
        "description": "Provide text alternatives for any non-text content so that it can be changed into other forms people need, such as large print, braille, speech, symbols or simpler language.",
        "principle": "1"
    },
    "1.2": {
        "name": "Time-based Media",
        "description": "Provide alternatives for time-based media.",
        "principle": "1"
    },
    "1.3": {
        "name": "Adaptable",
        "description": "Create content that can be presented in different ways without losing information or structure.",
        "principle": "1"
    },
    "1.4": {
        "name": "Distinguishable",
        "description": "Make it easier for users to see and hear content including separating foreground from background.",
        "principle": "1"
    },
    "2.1": {
        "name": "Keyboard Accessible",
        "description": "Make all functionality available from a keyboard.",
        "principle": "2"
    },
    "2.2": {
        "name": "Enough Time",
        "description": "Provide users enough time to read and use content.",
        "principle": "2"
    },
    "2.3": {
        "name": "Seizures and Physical Reactions",
        "description": "Do not design content in a way that is known to cause seizures or physical reactions.",
        "principle": "2"
    },
    "2.4": {
        "name": "Navigable",
        "description": "Provide ways to help users navigate, find content, and determine where they are.",
        "principle": "2"
    },
    "2.5": {
        "name": "Input Modalities",
        "description": "Make it easier for users to operate functionality through various inputs beyond keyboard.",
        "principle": "2"
    },
    "3.1": {
        "name": "Readable",
        "description": "Make text content readable and understandable.",
        "principle": "3"
    },
    "3.2": {
        "name": "Predictable",
        "description": "Make Web pages appear and operate in predictable ways.",
        "principle": "3"
    },
    "3.3": {
        "name": "Input Assistance",
        "description": "Help users avoid and correct mistakes.",
        "principle": "3"
    },
    "4.1": {
        "name": "Compatible",
        "description": "Maximize compatibility with current and future user agents, including assistive technologies.",
        "principle": "4"
    }
}


# Principles for WCAG 2.2
WCAG_22_PRINCIPLES = {
    "1": {
        "name": "Perceivable",
        "description": "Information and user interface components must be presentable to users in ways they can perceive."
    },
    "2": {
        "name": "Operable",
        "description": "User interface components and navigation must be operable."
    },
    "3": {
        "name": "Understandable",
        "description": "Information and the operation of user interface must be understandable."
    },
    "4": {
        "name": "Robust",
        "description": "Content must be robust enough that it can be interpreted by a wide variety of user agents, including assistive technologies."
    }
}


def slug_from_name(name: str) -> str:
    """Convert a success criterion name to a URL slug."""
    slug = name.lower()
    slug = slug.replace("(", "").replace(")", "")
    slug = slug.replace(",", "")
    slug = slug.replace(" - ", "-")
    slug = slug.replace(" ", "-")
    return slug


def build_sc_object(sc: dict, version: str = "2.2") -> dict:
    """Build a success criterion JSON-LD object."""
    sc_id = sc["id"]
    sc_name = sc["name"]
    sc_level = sc["level"]
    sc_slug = slug_from_name(sc_name)
    
    base_url = f"https://www.w3.org/TR/WCAG{version.replace('.', '')}/"
    understanding_base = f"https://www.w3.org/WAI/WCAG{version.replace('.', '')}/Understanding/"
    
    return {
        "@id": f"{base_url}#{sc_slug}",
        "@type": "SuccessCriterion",
        "identifier": sc_id,
        "name": sc_name,
        "level": sc_level,
        "understanding": f"{understanding_base}{sc_slug}.html"
    }


def generate_wcag_22() -> dict:
    """Generate complete WCAG 2.2 JSON-LD document."""
    
    # Build the structure
    principles = {}
    for p_id, p_data in WCAG_22_PRINCIPLES.items():
        principles[p_id] = {
            "@id": f"https://www.w3.org/TR/WCAG22/#{slug_from_name(p_data['name'])}",
            "@type": "Principle",
            "identifier": p_id,
            "name": p_data["name"],
            "description": p_data["description"],
            "guidelines": []
        }
    
    # Build guidelines with success criteria
    guidelines = {}
    for g_id, g_data in WCAG_22_GUIDELINES.items():
        guideline = {
            "@id": f"https://www.w3.org/TR/WCAG22/#{slug_from_name(g_data['name'])}",
            "@type": "Guideline",
            "identifier": g_id,
            "name": g_data["name"],
            "description": g_data["description"],
            "successCriteria": []
        }
        guidelines[g_id] = guideline
        
        # Add guideline to its principle
        principle_id = g_data["principle"]
        principles[principle_id]["guidelines"].append(guideline)
    
    # Add success criteria to guidelines
    for sc in WCAG_22_SUCCESS_CRITERIA:
        sc_obj = build_sc_object(sc, "2.2")
        guideline_id = sc["guideline"]
        
        # Find the guideline in the principles structure
        for principle in principles.values():
            for guideline in principle["guidelines"]:
                if guideline["identifier"] == guideline_id:
                    guideline["successCriteria"].append(sc_obj)
                    break
    
    # Build the complete document
    doc = {
        "@context": "https://raw.githubusercontent.com/mgifford/w3c-linkedobjects/main/schemas/context.jsonld",
        "@id": "https://www.w3.org/TR/WCAG22/",
        "@type": "Standard",
        "identifier": "WCAG 2.2",
        "title": "Web Content Accessibility Guidelines (WCAG) 2.2",
        "version": "2.2",
        "date": "2023-10-05",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/WCAG22/",
        "description": "Web Content Accessibility Guidelines (WCAG) 2.2 covers a wide range of recommendations for making Web content more accessible.",
        "principles": [principles[p_id] for p_id in sorted(principles.keys())],
        "metadata": {
            "extractedDate": datetime.now().strftime("%Y-%m-%d"),
            "totalSuccessCriteria": len(WCAG_22_SUCCESS_CRITERIA),
            "generatedBy": "scripts/generate-wcag.py",
            "newInVersion": [
                "2.4.11",
                "2.4.12",
                "2.4.13",
                "2.5.7",
                "2.5.8",
                "3.2.6",
                "3.3.7",
                "3.3.8",
                "3.3.9"
            ],
            "conformanceLevels": {
                "A": "Minimum level",
                "AA": "Recommended level for most content",
                "AAA": "Enhanced level"
            }
        }
    }
    
    return doc


def save_json_ld(data: dict, output_path: Path, indent: int = 2) -> None:
    """Save JSON-LD document to file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    
    print(f"✅ Generated: {output_path}")


def main():
    """Main generation function."""
    repo_root = Path(__file__).parent.parent
    
    print("WCAG JSON-LD Generator")
    print("=" * 60)
    
    # Generate WCAG 2.2
    print("\nGenerating WCAG 2.2...")
    wcag_22 = generate_wcag_22()
    output_path = repo_root / "standards" / "wcag-2.2.jsonld"
    save_json_ld(wcag_22, output_path)
    
    print(f"\n✅ Generated WCAG 2.2 with {wcag_22['metadata']['totalSuccessCriteria']} success criteria")
    print("\nNew success criteria in WCAG 2.2:")
    for sc_id in wcag_22['metadata']['newInVersion']:
        print(f"  - {sc_id}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
