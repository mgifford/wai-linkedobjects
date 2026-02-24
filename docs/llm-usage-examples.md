# Usage Examples for LLMs

This document provides practical examples of how to use w3c-linkedobjects with Large Language Models (LLMs) for accessibility code generation and review.

## Basic Usage Pattern

### 1. Include Standards Context

When asking an LLM to generate or review code, provide the relevant JSON-LD files as context:

```
I need you to review this React component for accessibility issues.

Context files:
- standards/wcag-2.2.jsonld (WCAG success criteria)
- standards/aria.jsonld (ARIA roles and properties)
- rules/axe-core.jsonld (automated testing rules)

Component code:
[paste your component code here]

Please identify any accessibility violations and provide:
1. The specific WCAG success criterion violated
2. The @id reference from the standards files
3. Recommended fix with code example
4. Related ARIA patterns if applicable
```

### 2. Request Explicit References

Always ask the LLM to cite specific identifiers:

```
For each accessibility recommendation, include:
- WCAG SC @id (e.g., "https://www.w3.org/TR/WCAG22/#non-text-content")
- ARIA @id if relevant (e.g., "https://www.w3.org/TR/wai-aria-1.2/#button")
- axe rule @id if applicable (e.g., "https://github.com/dequelabs/axe-core/.../button-name.json")
```

## Example 1: Button Accessibility Review

**Prompt:**
```
Review this button implementation for accessibility using w3c-linkedobjects standards.

Standards context:
- standards/wcag-2.2.jsonld
- standards/aria.jsonld
- rules/axe-core.jsonld

Code:
<div onclick="submitForm()">Submit</div>

Provide:
1. All violations with @id references
2. Severity (from axe rules)
3. Complete accessible implementation
```

**Expected LLM Response Structure:**
```
## Accessibility Violations

### 1. Missing Semantic Button Element
- **WCAG**: https://www.w3.org/TR/WCAG22/#name-role-value (4.1.2 Name, Role, Value)
- **WCAG**: https://www.w3.org/TR/WCAG22/#keyboard (2.1.1 Keyboard)
- **axe rule**: button-name (Impact: critical)
- **Issue**: Using div instead of button removes native keyboard accessibility

### 2. Missing Accessible Name
- **WCAG**: https://www.w3.org/TR/WCAG22/#name-role-value (4.1.2)
- **axe rule**: button-name
- **Issue**: Button has no discernible text or label

## Recommended Fix

<button type="button" onClick={submitForm}>
  Submit
</button>

## Rationale
- Uses semantic HTML <button> element
- Inherits role="button" from ARIA (https://www.w3.org/TR/wai-aria-1.2/#button)
- Has accessible name via text content
- Keyboard accessible by default (meets WCAG 2.1.1)
- Passes axe-core button-name rule
```

## Example 2: Image Alternative Text

**Prompt:**
```
Check this image implementation against WCAG 2.2 and axe rules.

Context: standards/wcag-2.2.jsonld, rules/axe-core.jsonld

<img src="logo.png">

Reference specific success criteria and rules by @id.
```

**Expected Response:**
```
## Violations

### Missing Alternative Text
- **WCAG SC**: https://www.w3.org/TR/WCAG22/#non-text-content (1.1.1 Non-text Content, Level A)
- **axe rule**: image-alt (https://github.com/dequelabs/axe-core/.../image-alt.json)
- **Impact**: Critical
- **Description**: Images must have alternate text (from axe rule)

## Fix

<img src="logo.png" alt="Company Logo">

If the image is decorative:
<img src="logo.png" alt="" role="presentation">
```

## Example 3: Form Label Association

**Prompt:**
```
Evaluate this form field for accessibility compliance.

Context:
- standards/wcag-2.2.jsonld
- standards/aria.jsonld  
- rules/axe-core.jsonld

<div>
  <span>Email:</span>
  <input type="email" name="email">
</div>

Cite violations using @id URIs from the standards.
```

**Expected Response:**
```
## Violations

### Missing Form Label Association
- **WCAG SC 1.3.1**: https://www.w3.org/TR/WCAG22/#info-and-relationships
- **WCAG SC 3.3.2**: https://www.w3.org/TR/WCAG22/#labels-or-instructions
- **WCAG SC 4.1.2**: https://www.w3.org/TR/WCAG22/#name-role-value
- **axe rule**: label (Impact: critical)

## Recommended Fixes

### Option 1: Explicit Label
<div>
  <label for="email">Email:</label>
  <input type="email" id="email" name="email">
</div>

### Option 2: ARIA Label
<div>
  <span id="email-label">Email:</span>
  <input 
    type="email" 
    name="email"
    aria-labelledby="email-label"
  >
</div>

References:
- HTML label element: https://html.spec.whatwg.org/#the-label-element
- ARIA labelledby: https://www.w3.org/TR/wai-aria-1.2/#aria-labelledby
```

## Example 4: Color Contrast Check

**Prompt:**
```
Using standards/wcag-2.2.jsonld and rules/axe-core.jsonld, evaluate:

<p style="color: #767676; background: #ffffff;">
  Important message
</p>

Provide WCAG SC @id and conformance level.
```

**Expected Response:**
```
## Potential Violation

### Insufficient Color Contrast
- **WCAG SC**: https://www.w3.org/TR/WCAG22/#contrast-minimum (1.4.3 Contrast Minimum)
- **Level**: AA
- **Requirement**: 4.5:1 for normal text
- **Actual**: 4.47:1 (borderline, may fail)
- **axe rule**: color-contrast (Impact: serious)

## Recommendation

Use darker text color:
<p style="color: #595959; background: #ffffff;">
  Important message
</p>

This provides 7:1 contrast ratio, meeting both:
- WCAG 2.2 SC 1.4.3 (AA - 4.5:1)
- WCAG 2.2 SC 1.4.6 (AAA - 7:1)
```

## Example 5: Complex Widget Pattern

**Prompt:**
```
Design an accessible tab panel using:
- standards/wcag-2.2.jsonld
- standards/aria.jsonld

Include all required ARIA attributes with @id references.
```

**Expected Response:**
```
## Accessible Tab Panel Implementation

<div role="tablist" aria-label="Content Sections">
  <button 
    role="tab" 
    aria-selected="true"
    aria-controls="panel-1"
    id="tab-1"
  >
    Section 1
  </button>
  <button 
    role="tab"
    aria-selected="false" 
    aria-controls="panel-2"
    id="tab-2"
    tabindex="-1"
  >
    Section 2
  </button>
</div>

<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">
  Content 1
</div>

<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
  Content 2
</div>

## Standards References

### ARIA Roles Used:
- tablist: https://www.w3.org/TR/wai-aria-1.2/#tablist
- tab: https://www.w3.org/TR/wai-aria-1.2/#tab
- tabpanel: https://www.w3.org/TR/wai-aria-1.2/#tabpanel

### ARIA Properties:
- aria-selected: https://www.w3.org/TR/wai-aria-1.2/#aria-selected (required for tab)
- aria-labelledby: https://www.w3.org/TR/wai-aria-1.2/#aria-labelledby (required for tabpanel)
- aria-controls: Links tab to its panel

### WCAG Success Criteria Met:
- 2.1.1 Keyboard: https://www.w3.org/TR/WCAG22/#keyboard
- 4.1.2 Name, Role, Value: https://www.w3.org/TR/WCAG22/#name-role-value

### Keyboard Support Needed:
- Arrow keys for tab navigation
- Home/End for first/last tab
- Tab key to enter panel content
```

## Tips for Best Results

1. **Be Specific**: Always reference the exact files you want the LLM to use
2. **Request Citations**: Ask for @id URIs to ensure traceability
3. **Ask for Severity**: Include impact levels from axe rules
4. **Request Alternatives**: Ask for multiple compliant solutions
5. **Validate Claims**: Cross-reference LLM output with the actual JSON-LD files

## Advanced Usage

### Combining Multiple Standards

```
Review this implementation against:
1. WCAG 2.2 success criteria (standards/wcag-2.2.jsonld)
2. ARIA best practices (standards/aria.jsonld)
3. axe-core rules (rules/axe-core.jsonld)
4. SiteImprove checks (rules/siteimprove.jsonld)

For each issue found, provide:
- All applicable @id references from all standards
- Highest severity level
- Most specific fix
```

### Generating Documentation

```
Using standards/wcag-2.2.jsonld and standards/aria.jsonld, generate
accessibility documentation for our button component that includes:

1. Which WCAG SCs it addresses (with @id)
2. ARIA patterns used (with @id)
3. Keyboard support requirements
4. Testing criteria from axe-core
```

## Common Pitfalls to Avoid

1. ❌ Not requesting @id references - LLM may hallucinate standards
2. ❌ Using only partial context - Include all relevant files
3. ❌ Not validating LLM output - Always cross-check references
4. ❌ Ignoring severity levels - Critical issues need immediate fixing
5. ❌ Accepting vague answers - Demand specific standard references

## Additional Resources

- W3C WAI: https://www.w3.org/WAI/
- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- ARIA 1.2: https://www.w3.org/TR/wai-aria-1.2/
- axe-core: https://github.com/dequelabs/axe-core
- SiteImprove Alfa: https://alfa.siteimprove.com/
