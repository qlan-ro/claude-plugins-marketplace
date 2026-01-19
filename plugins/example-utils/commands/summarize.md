# Summarize Command

Quickly summarize code, files, or selected content.

## Usage

```
/example-utils:summarize [file_path]
/example-utils:summarize  # summarizes current file
```

## Arguments

- `file_path` (optional): Path to the file to summarize. If not provided, summarize the current context.

## Instructions

When the user runs this command:

1. If a file path is provided, read that file
2. If no file path is provided, use the current file or recent context
3. Provide a concise summary including:
   - **Purpose**: What the code/file does (1-2 sentences)
   - **Key Components**: Main functions, classes, or sections
   - **Dependencies**: Notable imports or external dependencies
   - **Complexity**: Simple/Moderate/Complex assessment

Keep summaries brief and actionable. Use bullet points for clarity.

## Example Output

**Summary of `utils/parser.js`**

- **Purpose**: Parses configuration files and validates schemas
- **Key Components**:
  - `parseConfig()` - Main entry point
  - `validateSchema()` - JSON schema validation
  - `ConfigError` - Custom error class
- **Dependencies**: `ajv`, `fs-extra`
- **Complexity**: Moderate
