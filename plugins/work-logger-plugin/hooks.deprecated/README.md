# Deprecated Hooks (v1.x)

These hooks were used in v1.x to automatically log work activities.

**They are no longer needed in v2.0** because the plugin now parses AI assistant session history directly.

## Migration

If you were using these hooks:
1. No action needed - sessions are automatically parsed
2. Old work logs (if any) can still be read but are no longer generated
3. The new approach is more comprehensive and requires zero configuration

## Why Deprecated?

v1.x approach:
- Required hook configuration
- Only captured Claude Code tool uses
- Needed manual setup

v2.0 approach:
- Zero configuration
- Captures all AI assistants (Claude Code, Codex, Junie)
- Works automatically with session history
- Richer context about work

You can safely delete this directory.
