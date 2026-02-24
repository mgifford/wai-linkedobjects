# w3c-linkedobjects Quick Reference

## For LLMs: How to Use This Repository

When an LLM needs to provide accessibility guidance, include these files as context:

### Essential Files

1. **WCAG 2.2**: `standards/wcag-2.2.jsonld`
   - Contains success criteria for web accessibility
   - Organized by 4 principles: Perceivable, Operable, Understandable, Robust
   - Each criterion has @id, level (A/AA/AAA), and links to techniques

2. **ARIA**: `standards/aria.jsonld`
   - Contains roles (button, navigation, dialog, etc.)
   - Contains properties and states (aria-label, aria-expanded, etc.)
   - Each element has @id and links to related WCAG criteria

3. **axe-core Rules**: `rules/axe-core.jsonld`
   - Contains automated testing rules
   - Maps rules to WCAG success criteria
   - Includes impact levels (critical, serious, moderate, minor)

4. **SiteImprove Rules**: `rules/siteimprove.jsonld`
   - Additional accessibility checks
   - Categorized by type (aria, keyboard, forms, color, etc.)
   - Maps to WCAG criteria

### Context Schema

- `schemas/context.jsonld` - Defines the vocabulary and relationships used in all files

## Repository Map

```
standards/
├── wcag-2.2.jsonld      ← Core accessibility success criteria
├── aria.jsonld          ← ARIA roles, states, properties
├── atag.jsonld          ← (Future) Authoring tools
├── uaag.jsonld          ← (Future) User agents
├── html-a11y.jsonld     ← (Future) HTML accessibility
└── css-a11y.jsonld      ← (Future) CSS accessibility

rules/
├── axe-core.jsonld      ← Deque axe testing rules
└── siteimprove.jsonld   ← SiteImprove Alfa rules

schemas/
└── context.jsonld       ← JSON-LD vocabulary definitions

docs/
└── llm-usage-examples.md ← Detailed usage patterns

scripts/
├── fetch-standards.py   ← Monitor W3C updates
├── fetch-axe-rules.py   ← Monitor axe updates
└── validate.py          ← Validate JSON-LD files
```

## Key Identifiers in JSON-LD

Every resource has a unique `@id` URI that can be referenced:

### WCAG Success Criteria
```
https://www.w3.org/TR/WCAG22/#non-text-content
https://www.w3.org/TR/WCAG22/#name-role-value
https://www.w3.org/TR/WCAG22/#keyboard
```

### ARIA Roles
```
https://www.w3.org/TR/wai-aria-1.2/#button
https://www.w3.org/TR/wai-aria-1.2/#navigation
https://www.w3.org/TR/wai-aria-1.2/#dialog
```

### ARIA Properties
```
https://www.w3.org/TR/wai-aria-1.2/#aria-label
https://www.w3.org/TR/wai-aria-1.2/#aria-labelledby
https://www.w3.org/TR/wai-aria-1.2/#aria-describedby
```

## Example LLM Interaction

**Human:** "Review this button for accessibility"
```html
<div onclick="doThing()">Click me</div>
```

**LLM using this repository:**
```
I'll analyze this against the standards from w3c-linkedobjects:

VIOLATIONS FOUND:

1. Missing semantic button element
   - WCAG SC: https://www.w3.org/TR/WCAG22/#name-role-value (4.1.2)
   - WCAG SC: https://www.w3.org/TR/WCAG22/#keyboard (2.1.1)
   - axe rule: button-name (Impact: critical)
   - Issue: Using <div> instead of <button> breaks keyboard accessibility

2. No accessible name
   - WCAG SC: https://www.w3.org/TR/WCAG22/#name-role-value (4.1.2)
   - axe rule: button-name
   - Required: Button must have discernible text

RECOMMENDED FIX:
<button type="button" onClick={doThing}>Click me</button>

This meets:
- ARIA button role: https://www.w3.org/TR/wai-aria-1.2/#button
- WCAG 2.1.1 Keyboard (Level A)
- WCAG 4.1.2 Name, Role, Value (Level A)
- Passes axe-core button-name rule
```

## For Humans: Getting Started

1. Clone this repository
2. Browse `standards/wcag-2.2.jsonld` to see success criteria structure
3. Check `docs/llm-usage-examples.md` for detailed prompt patterns
4. Use `scripts/validate.py` to ensure JSON-LD validity

## For Developers

### Running Scripts

```bash
# Validate all JSON-LD files
python scripts/validate.py

# Check for W3C updates
python scripts/fetch-standards.py

# Check for axe updates  
python scripts/fetch-axe-rules.py
```

### CI/CD

GitHub Actions automatically:
- Validates JSON-LD on every push
- Checks for standards updates weekly
- Creates issues when updates are detected

## Resources

- **W3C WCAG**: https://www.w3.org/TR/WCAG22/
- **W3C ARIA**: https://www.w3.org/TR/wai-aria-1.2/
- **axe-core**: https://github.com/dequelabs/axe-core
- **SiteImprove Alfa**: https://alfa.siteimprove.com/

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on:
- Adding new standards
- Updating existing rules
- Improving documentation
- Reporting issues
