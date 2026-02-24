# w3c-linkedobjects

Machine-readable accessibility standards in JSON-LD format for AI systems.

This repository provides W3C WAI accessibility standards (WCAG, ATAG, UAAG, ARIA, HTML, CSS) and related testing rules (axe, SiteImprove) in structured JSON-LD format that LLMs can reliably consume when generating or reviewing code.

## What This Project Is For

- Give humans and LLMs a single, machine-readable source of truth for accessibility standards
- Reduce hallucinated or outdated accessibility advice by grounding responses in curated standards datasets
- Make relationships between standards explicit using linked data principles
- Support repeatable governance: validation, change monitoring, freshness checks, and CI guardrails
- Provide semantic web compatibility through JSON-LD format

## Why Use This With an LLM

If an LLM only sees your app code, it often gives generic accessibility advice.

If an LLM sees your app code plus this repository's structured standards context, it can:

- Map implementation choices to specific standards relationships
- Separate normative vs informative references
- Produce more auditable, standards-aligned recommendations
- Explain why a recommendation is being made via explicit links and evidence

## Repository Structure

```
standards/          # W3C accessibility standards in JSON-LD format
  wcag-2.2.jsonld   # WCAG 2.2 Success Criteria
  aria.jsonld       # ARIA roles, states, and properties
  atag.jsonld       # Authoring Tool Accessibility Guidelines
  uaag.jsonld       # User Agent Accessibility Guidelines
  html-a11y.jsonld  # HTML accessibility features
  css-a11y.jsonld   # CSS accessibility features

rules/              # Testing tool rules in JSON-LD format
  axe-core.jsonld   # Deque axe-core rules
  siteimprove.jsonld # SiteImprove accessibility rules

schemas/            # JSON-LD context and schemas
  context.jsonld    # Shared JSON-LD context

scripts/            # Automation scripts
  fetch-standards.py  # Fetch latest W3C standards
  fetch-axe-rules.py  # Fetch latest axe rules
  validate.py         # Validate JSON-LD documents

.github/workflows/  # CI/CD automation
```

## Quick Start

### For LLM Consumption

Point your LLM to the main standards files:

1. **WCAG 2.2**: `standards/wcag-2.2.jsonld` - Core accessibility success criteria
2. **ARIA**: `standards/aria.jsonld` - Accessible Rich Internet Applications
3. **Testing Rules**: `rules/axe-core.jsonld` - Automated testing rules

### Example LLM Prompt

```
Use my app code along with the accessibility standards from w3c-linkedobjects 
to propose accessible code changes. For each recommendation, include:
(a) relevant standard identifiers
(b) relationships to other standards
(c) confidence level of the support

Standards context:
- standards/wcag-2.2.jsonld
- standards/aria.jsonld
- rules/axe-core.jsonld
```

## Standards Included

### W3C Specifications
- **WCAG 2.2** (Web Content Accessibility Guidelines)
- **ARIA 1.2** (Accessible Rich Internet Applications)
- **ATAG 2.0** (Authoring Tool Accessibility Guidelines)
- **UAAG 2.0** (User Agent Accessibility Guidelines)
- **HTML** - Accessibility features from HTML Living Standard
- **CSS** - Accessibility-related CSS specifications

### Testing Rules
- **axe-core** - Deque axe accessibility testing rules
- **SiteImprove** - SiteImprove accessibility rules and checks

## Keeping Standards Up-to-Date

This repository uses GitHub Actions to automatically:

- Monitor W3C specifications for updates (weekly)
- Fetch latest axe-core rules (weekly)
- Check SiteImprove rule updates (weekly)
- Create pull requests when changes are detected

Manual updates can be triggered via:
```bash
python scripts/fetch-standards.py
python scripts/fetch-axe-rules.py
```

## JSON-LD Format

All standards use JSON-LD (JSON for Linked Data) format with:

- `@context` - Defines the semantic vocabulary
- `@id` - Unique identifier for each resource
- `@type` - Resource type classification
- Explicit links between related resources

Example:
```json
{
  "@context": "https://raw.githubusercontent.com/mgifford/w3c-linkedobjects/main/schemas/context.jsonld",
  "@id": "https://www.w3.org/TR/WCAG22/#non-text-content",
  "@type": "SuccessCriterion",
  "identifier": "1.1.1",
  "name": "Non-text Content",
  "level": "A",
  "relatedTo": ["https://www.w3.org/TR/wai-aria-1.2/#aria-label"]
}
```

## Documentation

- **[Document Relationships](docs/linked-relationships.md)** - Explains how ATAG, WCAG, and ARIA link together
- **[LLM Usage Examples](docs/llm-usage-examples.md)** - Detailed prompt patterns and examples
- **[Quick Reference](docs/index.md)** - Repository map and getting started guide

## Related Projects

- [wai-yaml-ld](https://github.com/mgifford/wai-yaml-ld) - YAML-based version of this project
- [W3C WAI](https://www.w3.org/WAI/) - Human-focused accessibility resources

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project compiles publicly available W3C specifications and testing rules. Please refer to the original sources for their respective licenses.

## Acknowledgments

This project builds upon the work of:
- W3C Web Accessibility Initiative (WAI)
- Deque Systems (axe-core)
- SiteImprove
- The wai-yaml-ld project
