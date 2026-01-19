#!/bin/bash
# Block access to sensitive files
# Exit codes: 0 = allow, 1 = error, 2 = block and tell Claude why

# Get file path from tool input (passed via stdin as JSON)
# For PreToolUse hooks, the input is JSON with tool_input.file_path
FILE_PATH="${1:-}"

# If no argument, try to read from stdin (JSON format)
if [ -z "$FILE_PATH" ]; then
  INPUT=$(cat)
  FILE_PATH=$(echo "$INPUT" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)"/\1/')
fi

# List of sensitive file patterns
BLOCKED_PATTERNS=(
  ".env"
  ".env.local"
  ".env.development"
  ".env.production"
  ".env.test"
  "secrets.json"
  "credentials.json"
  "service-account.json"
  "id_rsa"
  "id_ed25519"
  "*.pem"
  "*.key"
  ".aws/credentials"
  ".ssh/config"
  ".netrc"
  ".npmrc"
  ".pypirc"
)

# Check if the file matches any blocked pattern
for pattern in "${BLOCKED_PATTERNS[@]}"; do
  # Handle glob patterns
  if [[ "$pattern" == *"*"* ]]; then
    if [[ "$FILE_PATH" == $pattern ]]; then
      echo "BLOCKED: Access to '$FILE_PATH' denied for security reasons." >&2
      echo "This file may contain sensitive credentials or secrets." >&2
      echo "If you need to work with environment variables, edit .env.example instead." >&2
      exit 2
    fi
  else
    # Handle exact matches and path endings
    if [[ "$FILE_PATH" == *"$pattern" ]] || [[ "$FILE_PATH" == *"/$pattern" ]]; then
      echo "BLOCKED: Access to '$FILE_PATH' denied for security reasons." >&2
      echo "This file may contain sensitive credentials or secrets." >&2
      echo "If you need to work with environment variables, edit .env.example instead." >&2
      exit 2
    fi
  fi
done

# Allow the operation
exit 0
