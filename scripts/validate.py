#!/usr/bin/env python3
"""
Validation script for JSON-LD documents.

This script validates all JSON-LD files in the repository to ensure
they are well-formed and contain required fields.
"""

import json
import sys
from pathlib import Path
from typing import List, Tuple


def validate_json_ld(file_path: Path) -> Tuple[bool, List[str]]:
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
