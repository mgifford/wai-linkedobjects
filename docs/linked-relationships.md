# Document Relationships in w3c-linkedobjects

This document explains how the w3c-linkedobjects repository models relationships between W3C standards using JSON-LD linked data principles.

## Overview

The repository uses JSON-LD (JSON for Linked Data) to create explicit, machine-readable relationships between accessibility standards. This allows AI systems, tools, and developers to understand how different standards relate to and reference each other.

## Key Relationship Properties

### 1. `relatedTo`

The `relatedTo` property creates general semantic relationships between resources. It uses URIs (@id) to point to related standards, guidelines, or success criteria.

**Semantic Mapping**: `skos:related` (from SKOS vocabulary)

**Example**: ATAG references WCAG
```json
{
  "@id": "https://www.w3.org/TR/ATAG20/#sc_a111",
  "identifier": "A.1.1.1",
  "name": "Web-Based Accessible",
  "relatedTo": [
    "https://www.w3.org/TR/WCAG22/#conformance"
  ]
}
```

### 2. `wcagCriteria`

The `wcagCriteria` property specifically links testing rules or implementation techniques to WCAG success criteria. This creates explicit mappings between automated testing and normative requirements.

**Semantic Mapping**: `wcag:relatedSuccessCriterion`

**Example**: Testing rule mapped to WCAG
```json
{
  "ruleId": "button-name",
  "wcagCriteria": [
    "https://www.w3.org/TR/WCAG22/#name-role-value"
  ]
}
```

### 3. `techniques`

The `techniques` property links WCAG success criteria to implementation techniques and examples.

**Semantic Mapping**: `wcag:technique`

**Example**: WCAG success criterion with techniques
```json
{
  "@id": "https://www.w3.org/TR/WCAG22/#non-text-content",
  "techniques": [
    "https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA6",
    "https://www.w3.org/WAI/WCAG22/Techniques/html/H37"
  ]
}
```

### 4. `inheritsFrom`

The `inheritsFrom` property models inheritance relationships, particularly for ARIA roles.

**Semantic Mapping**: `schema:subClassOf`

**Example**: ARIA role hierarchy
```json
{
  "@id": "https://www.w3.org/TR/wai-aria-1.2/#alertdialog",
  "name": "alertdialog",
  "inheritsFrom": "https://www.w3.org/TR/wai-aria-1.2/#alert"
}
```

## Real-World Examples

### Example 1: ATAG → WCAG Relationship

ATAG (Authoring Tool Accessibility Guidelines) references WCAG throughout its guidelines to ensure that authoring tools both:
1. Have accessible user interfaces (Part A)
2. Enable creation of accessible content (Part B)

**ATAG Success Criterion A.1.1.1** (in `standards/atag.jsonld`):
```json
{
  "@id": "https://www.w3.org/TR/ATAG20/#sc_a111",
  "@type": "SuccessCriterion",
  "identifier": "A.1.1.1",
  "name": "Web-Based Accessible",
  "level": "A",
  "description": "If the authoring tool is web-based, then it conforms to WCAG 2.0 Level A.",
  "relatedTo": [
    "https://www.w3.org/TR/WCAG22/#conformance"
  ]
}
```

This shows that ATAG A.1.1.1 requires conformance to WCAG's conformance requirements.

### Example 2: WCAG → ARIA Relationship

WCAG (Web Content Accessibility Guidelines) references ARIA as an implementation technique for achieving accessibility requirements.

**WCAG Success Criterion 1.1.1** (in `standards/wcag-2.2.jsonld`):
```json
{
  "@id": "https://www.w3.org/TR/WCAG22/#non-text-content",
  "@type": "SuccessCriterion",
  "identifier": "1.1.1",
  "name": "Non-text Content",
  "level": "A",
  "techniques": [
    "https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA6",
    "https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA10"
  ],
  "relatedTo": [
    "https://www.w3.org/TR/wai-aria-1.2/#aria-label",
    "https://www.w3.org/TR/wai-aria-1.2/#aria-labelledby"
  ]
}
```

This shows that:
- ARIA techniques (ARIA6, ARIA10) can be used to meet WCAG 1.1.1
- ARIA properties (`aria-label`, `aria-labelledby`) are related mechanisms

### Example 3: ARIA → WCAG Relationship

ARIA roles and properties reference WCAG success criteria they help satisfy.

**ARIA button role** (in `standards/aria.jsonld`):
```json
{
  "@id": "https://www.w3.org/TR/wai-aria-1.2/#button",
  "@type": "Role",
  "name": "button",
  "relatedTo": [
    "https://html.spec.whatwg.org/#the-button-element",
    "https://www.w3.org/TR/WCAG22/#keyboard"
  ]
}
```

This shows that the ARIA button role relates to:
- The HTML `<button>` element (same semantic meaning)
- WCAG keyboard requirements (buttons must be keyboard accessible)

## Complete Chain: ATAG → WCAG → ARIA

Here's how the complete chain works:

```
ATAG 2.0 (Guideline B.2.2)
    ↓ relatedTo
WCAG 2.2 (Success Criterion 1.1.1)
    ↓ relatedTo
ARIA 1.2 (aria-label property)
```

**Tracing the chain**:

1. **ATAG B.2.2.1** requires authoring tools to provide accessible markup options
   - Links to → WCAG 1.1.1 (Non-text Content)

2. **WCAG 1.1.1** requires text alternatives for non-text content
   - Links to → ARIA `aria-label` and `aria-labelledby`

3. **ARIA** provides the mechanism (`aria-label`) to implement the requirement

This creates a traceable path from authoring tool requirements, through content requirements, to implementation mechanisms.

## Benefits for AI Systems

### 1. Explainability
AI systems can trace recommendations back to normative requirements:
```
"Use aria-label because:
  - WCAG 1.1.1 requires text alternatives
  - WCAG 1.1.1 is referenced by ATAG B.2.2.1
  - This ensures both content AND authoring tools are accessible"
```

### 2. Consistency
All relationships use URI-based linking, enabling:
- Graph queries across standards
- Automated consistency checking
- Bidirectional navigation

### 3. Validation
Testing tools can validate implementations against the full chain:
```
Test: Does button have aria-label?
  ↓
Maps to: WCAG 4.1.2 (Name, Role, Value)
  ↓
Required by: ATAG A.1.2.1 (Platform Accessibility Services)
```

## Using Relationships in Queries

### Example 1: Find all WCAG criteria referenced by ATAG
```json
Query: All resources with relatedTo pointing to WCAG22 URIs
Result: ATAG success criteria that reference WCAG
```

### Example 2: Find implementation techniques for a WCAG criterion
```json
Query: WCAG 1.1.1 -> techniques property
Result: List of ARIA and HTML techniques
```

### Example 3: Find standards hierarchy
```json
Query: Follow relatedTo from ATAG -> WCAG -> ARIA -> HTML
Result: Complete implementation chain
```

## Adding New Relationships

When adding new standards or updating existing ones:

1. **Use `relatedTo`** for general cross-references
2. **Use `wcagCriteria`** for explicit WCAG mappings (especially in testing rules)
3. **Use `techniques`** for implementation guidance
4. **Use `inheritsFrom`** for hierarchical relationships
5. **Always use full URIs** as @id values for unambiguous references

### Example Template
```json
{
  "@id": "https://example.org/standard/#requirement-1",
  "@type": "SuccessCriterion",
  "identifier": "1.0.0",
  "name": "Requirement Name",
  "relatedTo": [
    "https://www.w3.org/TR/WCAG22/#conformance",
    "https://www.w3.org/TR/wai-aria-1.2/#aria-label"
  ]
}
```

## Semantic Web Compatibility

All relationships are defined in `schemas/context.jsonld` using standard vocabularies:

- **SKOS** (Simple Knowledge Organization System): `relatedTo` maps to `skos:related`
- **Schema.org**: General metadata and relationships
- **Dublin Core**: Bibliographic metadata
- **W3C WCAG/ARIA namespaces**: Domain-specific terms

This ensures compatibility with semantic web tools, RDF processors, and linked data systems.

## Querying Examples for LLMs

### Example Prompt 1: Understanding Relationships
```
"Looking at standards/atag.jsonld, show me all ATAG success criteria 
that reference WCAG success criterion 1.1.1 (Non-text Content)"
```

**Expected Response**: List of ATAG success criteria with @id and relatedTo fields pointing to WCAG 1.1.1

### Example Prompt 2: Implementation Chain
```
"Trace the implementation chain from ATAG B.2.2.1 to ARIA properties.
Show each step with @id URIs."
```

**Expected Response**: 
```
ATAG B.2.2.1 (https://www.w3.org/TR/ATAG20/#sc_b221)
  → relatedTo → WCAG 1.1.1 (https://www.w3.org/TR/WCAG22/#non-text-content)
  → relatedTo → ARIA aria-label (https://www.w3.org/TR/wai-aria-1.2/#aria-label)
```

### Example Prompt 3: Compliance Checking
```
"Given a button element with aria-label, show which standards 
requirements this satisfies by following the relationship chain"
```

**Expected Response**: List of satisfied requirements across ARIA → WCAG → ATAG with URIs

## Conclusion

The w3c-linkedobjects repository uses JSON-LD relationships to create an explicit, traceable network of connections between W3C accessibility standards. This enables AI systems, tools, and developers to:

- Understand how standards relate to each other
- Trace requirements from high-level guidelines to implementation details
- Validate implementations against the full standards chain
- Provide explainable, standards-based recommendations

The relationships are bidirectional, semantically defined, and compatible with standard linked data tools, making them suitable for both human and machine consumption.
