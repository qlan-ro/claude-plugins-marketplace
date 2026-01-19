# Explain Command

Get a detailed explanation of code with examples.

## Usage

```
/example-utils:explain [file_path_or_concept]
/example-utils:explain  # explains current selection or file
```

## Arguments

- `file_path_or_concept` (optional): A file path, function name, or concept to explain.

## Instructions

When the user runs this command:

1. Identify what needs to be explained (file, function, concept, or selected code)
2. Provide a thorough explanation including:

### For Code:
- **What it does**: Clear description of functionality
- **How it works**: Step-by-step breakdown of the logic
- **Parameters/Inputs**: What the code expects
- **Returns/Outputs**: What the code produces
- **Example Usage**: Practical code examples
- **Edge Cases**: Important considerations

### For Concepts:
- **Definition**: Clear, simple definition
- **Why it matters**: Practical importance
- **Example**: Concrete implementation example
- **Related concepts**: Links to related topics

## Example Output

**Explaining `debounce` function**

**What it does**: Limits how often a function can be called by waiting for a pause in invocations.

**How it works**:
1. When called, it starts a timer
2. If called again before timer expires, timer resets
3. Function only executes after timer completes without interruption

**Example Usage**:
```javascript
const debouncedSearch = debounce(searchAPI, 300);
input.addEventListener('input', debouncedSearch);
```

**When to use**: Search inputs, window resize handlers, autosave features.
