# Contributing to w3c-linkedobjects

Thank you for your interest in contributing to w3c-linkedobjects! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

If you find an issue with the standards data or tooling:

1. Check if the issue already exists
2. Create a new issue with a clear title and description
3. Include relevant details like file paths, expected vs actual behavior
4. Tag with appropriate labels (bug, enhancement, documentation, etc.)

### Suggesting Enhancements

We welcome suggestions for:

- New W3C standards to include
- Additional testing rule sources (beyond axe and SiteImprove)
- Improvements to JSON-LD structure
- Better documentation

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run validation: `python scripts/validate.py`
5. Commit your changes with clear commit messages
6. Push to your branch
7. Open a Pull Request

## JSON-LD Structure Guidelines

All JSON-LD files should follow these conventions:

### Required Fields

Every JSON-LD document must include:

```json
{
  "@context": "https://raw.githubusercontent.com/mgifford/w3c-linkedobjects/main/schemas/context.jsonld",
  "@id": "unique-identifier-uri",
  "@type": "Standard",
  "identifier": "short-id",
  "title": "Human-readable title",
  "version": "version-number",
  "date": "YYYY-MM-DD",
  "publisher": "Publisher name",
  "url": "canonical-url",
  "description": "Brief description"
}
```

### Linking Standards

Use `relatedTo` and `wcagCriteria` to link between resources:

```json
{
  "relatedTo": [
    "https://www.w3.org/TR/wai-aria-1.2/#button"
  ],
  "wcagCriteria": [
    "https://www.w3.org/TR/WCAG22/#name-role-value"
  ]
}
```

### Property Naming

- Use camelCase for property names
- Use URIs for @id values
- Use standard vocabularies from the context

## Updating Standards

### W3C Standards

When W3C publishes a new version:

1. Update the version and date fields
2. Add new success criteria, guidelines, or roles
3. Maintain backward compatibility when possible
4. Document breaking changes in the PR description

### Testing Rules

When axe or SiteImprove updates their rules:

1. Check the official changelog
2. Add new rules with proper structure
3. Update rule descriptions and mappings
4. Ensure WCAG criteria links are accurate

## Testing

Before submitting a PR:

```bash
# Validate all JSON-LD files
python scripts/validate.py

# Check W3C standards status
python scripts/fetch-standards.py

# Check axe rules status
python scripts/fetch-axe-rules.py
```

## Code Style

### Python Scripts

- Follow PEP 8
- Use type hints
- Include docstrings
- Handle exceptions gracefully

### JSON-LD Files

- Use 2-space indentation
- Keep consistent ordering of fields
- Format with proper line breaks for readability

## Questions?

- Open an issue for general questions
- Tag maintainers for urgent matters
- Check existing issues and PRs first

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
