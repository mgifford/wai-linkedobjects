# AGENTS.md

This file provides guidance for AI coding agents working in this repository.

## Python Development

All Python scripts in this project (under `scripts/`) must follow the
conventions described in [PYTHON_GUIDANCE.md](PYTHON_GUIDANCE.md).

Key points:
- Use 4-space indentation and `snake_case` names (PEP 8).
- Annotate every function signature with type hints.
- Write a docstring for every module, class, and function (including `main()`).
- Never use a bare `except:`; always catch specific exception types.
- Keep functions ≤ 50 lines; split longer functions into focused helpers.
- Place all `import` statements at the top of the file.
- Prefer `pathlib.Path` over `os.path` / `os.makedirs` for file-system operations.
- Run `flake8 scripts/` (or `ruff check scripts/`) before every commit and
  resolve all warnings.

## Repository Layout

| Path | Purpose |
|------|---------|
| `scripts/` | Python helper scripts (fetch, validate, generate) |
| `standards/` | Generated JSON-LD documents for W3C standards |
| `schemas/` | JSON-LD context and schema definitions |
| `rules/` | Rule definitions |
| `docs/` | Additional documentation |

## Running the Scripts

```bash
# Validate all JSON-LD files
python scripts/validate.py

# Generate WCAG 2.2 JSON-LD
python scripts/generate-wcag.py

# Fetch latest axe-core rules
python scripts/fetch-axe-rules.py

# Fetch latest W3C standards status
python scripts/fetch-standards.py
```

## Dependencies

Install all Python dependencies before running any script:

```bash
pip install -r requirements.txt
```
