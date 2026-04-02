#!/usr/bin/env python3
"""
Validation script for JSON-LD documents.

This script validates all JSON-LD files in the repository to ensure
they are well-formed and contain required fields.

For WCAG standards, it also validates completeness:
- Checks that success criteria count matches metadata
- Verifies required success criteria are present
"""

import json
import sys
from pathlib import Path


def count_success_criteria(data: dict) -> int:
    """Count all success criteria in a WCAG document."""
    count = 0
    
    if "principles" in data:
        for principle in data["principles"]:
            if "guidelines" in principle:
                for guideline in principle["guidelines"]:
                    if "successCriteria" in guideline:
                        count += len(guideline["successCriteria"])
    
    return count


def extract_sc_identifiers(data: dict) -> set[str]:
    """Extract all success criterion identifiers from a WCAG document."""
    identifiers = set()
    
    if "principles" in data:
        for principle in data["principles"]:
            if "guidelines" in principle:
                for guideline in principle["guidelines"]:
                    if "successCriteria" in guideline:
                        for sc in guideline["successCriteria"]:
                            if "identifier" in sc:
                                identifiers.add(sc["identifier"])
    
    return identifiers


def validate_wcag_completeness(data: dict, file_name: str) -> list[str]:
    """
    Validate WCAG document completeness.
    
    Checks:
    - Success criteria count matches metadata
    - Required success criteria are present (e.g., 4.1.3 Status Messages)
    """
    errors = []
    
    # Count actual success criteria
    actual_count = count_success_criteria(data)
    
    # Check metadata count
    if "metadata" in data and "totalSuccessCriteria" in data["metadata"]:
        expected_count = data["metadata"]["totalSuccessCriteria"]
        
        if actual_count != expected_count:
            errors.append(
                f"Success criteria count mismatch: "
                f"found {actual_count}, metadata claims {expected_count}"
            )
    
    # Extract SC identifiers
    sc_ids = extract_sc_identifiers(data)
    
    # Check for critical success criteria that were historically missing
    critical_scs = {
        "4.1.3": "Status Messages (Level AA, WCAG 2.1+)"
    }
    
    # Only check for 4.1.3 in WCAG 2.1 and 2.2
    if "wcag-2.2" in file_name or "wcag-2.1" in file_name:
        for sc_id, sc_name in critical_scs.items():
            if sc_id not in sc_ids:
                errors.append(f"Missing required SC {sc_id}: {sc_name}")
    
    # Verify no duplicate identifiers
    if actual_count != len(sc_ids):
        errors.append(
            f"Duplicate success criteria detected: "
            f"{actual_count} SCs found but only {len(sc_ids)} unique identifiers"
        )
    
    return errors


def validate_json_ld(file_path: Path) -> tuple[bool, list[str]]:
    """
    Validate a JSON-LD file.
    
    Returns:
        Tuple of (is_valid, list of errors)
    """
    errors = []
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Skip validation for context definition files
        if file_path.name == "context.jsonld" and "@context" in data:
            # This is a context definition, just check it's valid JSON
            return True, []
        
        # Check for required JSON-LD fields
        if "@context" not in data:
            errors.append("Missing @context")
        
        if "@id" not in data:
            errors.append("Missing @id")
        
        if "@type" not in data:
            errors.append("Missing @type")
        
        # Check for basic metadata
        if "identifier" not in data:
            errors.append("Missing identifier")
        
        if "title" not in data:
            errors.append("Missing title")
        
        if "description" not in data:
            errors.append("Missing description")
        
        # WCAG-specific validation
        if "wcag" in file_path.name.lower() and "principles" in data:
            wcag_errors = validate_wcag_completeness(data, file_path.name)
            errors.extend(wcag_errors)
        
        return len(errors) == 0, errors
        
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON: {e}")
        return False, errors
    except Exception as e:
        errors.append(f"Error reading file: {e}")
        return False, errors


def validate_all_jsonld_files(base_path: Path) -> bool:
    """
    Validate all JSON-LD files in the repository.
    
    Returns:
        True if all files are valid, False otherwise
    """
    all_valid = True
    jsonld_files = list(base_path.glob("**/*.jsonld"))
    
    if not jsonld_files:
        print("⚠️  No JSON-LD files found")
        return False
    
    print(f"Validating {len(jsonld_files)} JSON-LD files...\n")
    
    for file_path in jsonld_files:
        is_valid, errors = validate_json_ld(file_path)
        
        if is_valid:
            print(f"✅ {file_path.relative_to(base_path)}")
            
            # Show WCAG statistics for WCAG files
            if "wcag" in file_path.name.lower():
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    if "principles" in data:
                        sc_count = count_success_criteria(data)
                        print(f"   └─ {sc_count} success criteria")
                except Exception:
                    pass
        else:
            print(f"❌ {file_path.relative_to(base_path)}")
            for error in errors:
                print(f"   - {error}")
            all_valid = False
    
    return all_valid


def main():
    """Main validation function."""
    # Get the repository root
    repo_root = Path(__file__).parent.parent
    
    print("JSON-LD Validation")
    print("=" * 60)
    
    all_valid = validate_all_jsonld_files(repo_root)
    
    print("\n" + "=" * 60)
    if all_valid:
        print("✅ All JSON-LD files are valid")
        sys.exit(0)
    else:
        print("❌ Some JSON-LD files have validation errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
