# Quick Docs Skill

Automatically generates documentation for functions, classes, and modules.

## Description

Quick Docs analyzes code and generates appropriate documentation in the correct format for the language (JSDoc, docstrings, XML comments, etc.).

## Trigger Conditions

This skill activates when users:
- Ask to "document this function/class/code"
- Request "add documentation"
- Say "generate docs" or "add JSDoc/docstring"
- Ask for "API documentation"

## Capabilities

### Supported Languages
- JavaScript/TypeScript (JSDoc)
- Python (docstrings - Google, NumPy, or Sphinx style)
- Java (Javadoc)
- C# (XML documentation)
- Go (godoc comments)
- Rust (rustdoc)
- Ruby (YARD)
- PHP (PHPDoc)

### Documentation Includes
- Function/method description
- Parameter descriptions with types
- Return value description
- Throws/raises documentation
- Example usage (when helpful)
- Deprecation notices (when applicable)

## Instructions

When generating documentation:

1. **Analyze the code** to understand its purpose
2. **Detect the language** and use appropriate format
3. **Be concise but complete** - describe what, not how
4. **Include types** even in dynamically typed languages
5. **Add examples** for complex functions
6. **Note side effects** and important behaviors

## Example

**Input:**
```javascript
function calculateDiscount(price, percentage, maxDiscount) {
  const discount = price * (percentage / 100);
  return Math.min(discount, maxDiscount);
}
```

**Output:**
```javascript
/**
 * Calculates a discount amount, capped at a maximum value.
 *
 * @param {number} price - The original price
 * @param {number} percentage - The discount percentage (0-100)
 * @param {number} maxDiscount - Maximum allowed discount amount
 * @returns {number} The calculated discount, not exceeding maxDiscount
 *
 * @example
 * calculateDiscount(100, 20, 15) // Returns 15 (capped)
 * calculateDiscount(100, 10, 15) // Returns 10
 */
function calculateDiscount(price, percentage, maxDiscount) {
  const discount = price * (percentage / 100);
  return Math.min(discount, maxDiscount);
}
```

## Configuration

Default style preferences can be set in plugin config:

```json
{
  "quickDocs": {
    "pythonStyle": "google",
    "includeExamples": true,
    "includeTypes": true
  }
}
```
