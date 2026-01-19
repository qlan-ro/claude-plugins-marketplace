# My Claude Code Plugin Marketplace

A personal collection of Claude Code plugins for enhanced development workflows.

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
| [example-utils](./plugins/example-utils) | Utility commands and helpers | 1.0.0 |

## Directory Structure

```
claude-plugins-marketplace/
├── README.md                    # This file
├── plugins/                     # All plugins live here
│   └── example-utils/           # Example plugin
│       ├── .claude-plugin/
│       │   └── plugin.json      # Plugin metadata
│       ├── commands/            # Slash commands
│       ├── agents/              # Specialized agents
│       ├── skills/              # Agent skills
│       ├── hooks/               # Event handlers
│       └── README.md            # Plugin documentation
└── templates/                   # Templates for creating new plugins
    └── basic-plugin/            # Basic plugin template
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
