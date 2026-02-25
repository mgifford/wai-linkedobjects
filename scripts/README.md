# Scripts

This directory contains automation scripts for managing W3C accessibility standards in JSON-LD format.

## Available Scripts

### `generate-wcag.py`

Generates complete WCAG JSON-LD files with all success criteria inline.

**Features:**
- Uses a comprehensive static reference of all WCAG success criteria
- Generates complete WCAG 2.2 with all 86 success criteria
- Ensures faithful representation of the W3C standard
- Includes proper Understanding URLs for each SC
- Can be extended for WCAG 2.1 and other versions

**Usage:**
```bash
python scripts/generate-wcag.py
```

**Output:**
- `standards/wcag-2.2.jsonld` - Complete WCAG 2.2 JSON-LD file

### `validate.py`

Validates all JSON-LD files in the repository.

**Features:**
- Checks required JSON-LD fields (@context, @id, @type)
- Validates basic metadata (identifier, title, description)
- **WCAG-specific validation:**
  - Verifies success criteria count matches metadata
  - Checks for required SCs (e.g., 4.1.3 Status Messages)
  - Detects duplicate SC identifiers
- Reports statistics for WCAG files

**Usage:**
```bash
python scripts/validate.py
```

**Exit codes:**
- `0` - All files valid
- `1` - Validation errors found

### `fetch-standards.py`

Monitors W3C accessibility standards for updates.

**Features:**
- Checks WCAG, ARIA, ATAG, and UAAG specifications
- Records Last-Modified headers and ETags
- Creates status reports

**Usage:**
```bash
python scripts/fetch-standards.py
```

### `fetch-axe-rules.py`

Fetches and processes axe-core accessibility rules.

## GitHub Actions Workflows

### Generate WCAG Standards (`.github/workflows/generate-wcag.yml`)

Automatically generates WCAG standards and creates a PR if changes are detected.

**Triggers:**
- Manual workflow dispatch
- Quarterly schedule (1st of every 3rd month)

**What it does:**
1. Runs `generate-wcag.py` to regenerate WCAG files
2. Validates the generated files
3. Creates a PR if changes are detected

### Validate JSON-LD (`.github/workflows/validate.yml`)

Validates all JSON-LD files on every push and PR.

**Triggers:**
- Push to main or copilot/** branches
- Pull requests to main
- Changes to .jsonld files or validation scripts

## Development

### Adding New Success Criteria

To add or update success criteria in WCAG 2.2, edit the `WCAG_22_SUCCESS_CRITERIA` list in `generate-wcag.py`.

Each SC entry should include:
```python
{"id": "X.X.X", "name": "SC Name", "level": "A/AA/AAA", "guideline": "X.X"}
```

### Extending to WCAG 2.1

To add WCAG 2.1 generation:
1. Create `WCAG_21_SUCCESS_CRITERIA` list (78 SCs)
2. Add corresponding guidelines and principles
3. Create `generate_wcag_21()` function
4. Update `main()` to generate both versions

## Requirements

All scripts require dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Completeness Guarantee

The generator and validator work together to ensure:
- All success criteria are present
- No duplicates exist
- Metadata counts match actual counts
- Critical SCs like 4.1.3 Status Messages are not missed
- Understanding URLs point to the correct WCAG version
