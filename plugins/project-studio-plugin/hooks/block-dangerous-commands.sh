#!/bin/bash
# Block dangerous shell commands
# Exit codes: 0 = allow, 1 = error, 2 = block and tell Claude why

# Get command from tool input (passed via stdin as JSON or as argument)
COMMAND="${1:-}"

# If no argument, try to read from stdin (JSON format)
if [ -z "$COMMAND" ]; then
  INPUT=$(cat)
  COMMAND=$(echo "$INPUT" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/"command"[[:space:]]*:[[:space:]]*"\([^"]*\)"/\1/')
fi

# Dangerous patterns that require explicit user confirmation
# These are blocked because CLAUDE.md rules can be ignored under context pressure
DANGEROUS_PATTERNS=(
  # Destructive file operations
  "rm -rf /"
  "rm -rf /*"
  "rm -rf ~"
  "rm -rf ~/"
  "> /dev/sda"
  "mkfs."

  # Dangerous git operations
  "git push --force"
  "git push -f"
  "git reset --hard"
  "git clean -fdx"

  # Skip safety checks
  "--no-verify"
  "--skip-hooks"

  # Database destruction
  "DROP DATABASE"
  "DROP TABLE"
  "TRUNCATE"

  # System modification
  "chmod -R 777"
  "chmod 777"
  "sudo rm"

  # Network exfiltration patterns
  "curl.*|.*sh"
  "wget.*|.*sh"
)

# Check for dangerous patterns
for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if [[ "$COMMAND" == *"$pattern"* ]]; then
    echo "BLOCKED: Dangerous command detected: '$pattern'" >&2
    echo "This command could cause irreversible damage or bypass safety checks." >&2
    echo "If you really need to run this, ask the user to execute it manually." >&2
    exit 2
  fi
done

# Special check for force push to main/master
if [[ "$COMMAND" =~ "git push".*"--force".*"main" ]] || [[ "$COMMAND" =~ "git push".*"--force".*"master" ]] || \
   [[ "$COMMAND" =~ "git push".*"-f".*"main" ]] || [[ "$COMMAND" =~ "git push".*"-f".*"master" ]]; then
  echo "BLOCKED: Force push to main/master branch detected." >&2
  echo "This is an extremely dangerous operation that can cause data loss." >&2
  echo "If you really need to do this, ask the user to execute it manually." >&2
  exit 2
fi

# Special check for hard reset with remote
if [[ "$COMMAND" =~ "git reset --hard origin" ]]; then
  echo "BLOCKED: Hard reset to remote branch detected." >&2
  echo "This will discard all local changes permanently." >&2
  echo "If you really need to do this, ask the user to execute it manually." >&2
  exit 2
fi

# Allow the operation
exit 0
