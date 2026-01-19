# QLAN Claude Code Plugin Marketplace

A collection of Claude Code plugins for enhanced development workflows by QLAN Software Solutions.

## Installation

Add this marketplace to Claude Code:

```bash
claude plugins:add https://github.com/qlan-ro/claude-plugins-marketplace
```

Or install individual plugins:

```bash
claude plugins:install github:qlan-ro/claude-plugins-marketplace/plugins/PLUGIN_NAME
```

## Available Plugins

| Plugin | Description | Version |
|--------|-------------|---------|
| [project-studio](./plugins/project-studio-plugin) | Full-stack product development orchestration with PRD building, architecture design, UX design, and implementation planning | 1.0.0 |
| [work-logger](./plugins/work-logger-plugin) | Generates Slack status messages from AI assistant session history (Claude Code, Codex, Junie) | 2.0.0 |

## Directory Structure

```
claude-plugins-marketplace/
├── .claude-plugin/
│   └── marketplace.json         # Marketplace registry (lists all plugins)
├── README.md                    # This file
├── plugins/
│   ├── project-studio-plugin/   # Product development orchestration
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── agents/              # PRD, architect, designer agents
│   │   ├── commands/            # new-project, add-feature, phase, gate-check
│   │   ├── skills/              # orchestration, prd-discovery, ux-design
│   │   ├── hooks/               # Validation hooks
│   │   └── references/          # Phase guides and checklists
│   └── work-logger-plugin/      # Slack status generator
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── commands/            # slack-status command
│       ├── skills/              # slack-status-writer skill
│       └── parsers/             # Session parsers (Claude, Codex, Junie)
└── templates/
    └── basic-plugin/            # Template for new plugins
```

## Creating a New Plugin

1. Copy the template:
   ```bash
   cp -r templates/basic-plugin plugins/my-new-plugin
   ```

2. Edit `plugins/my-new-plugin/.claude-plugin/plugin.json` with your plugin details

3. Add your commands, agents, skills, or hooks

4. Update the plugins table in this README

## Plugin Components

- **Commands**: Custom slash commands (Markdown files in `commands/`)
- **Agents**: Specialized AI assistants (in `agents/`)
- **Skills**: Auto-invoked capabilities (in `skills/`)
- **Hooks**: Event-triggered automation (in `hooks/`)
- **MCP**: External tool integrations (`.mcp.json`)

## License

MIT License - Feel free to use and modify these plugins.
