#!/usr/bin/env python3
"""
Parser for Claude Code project sessions stored in ~/.claude/projects/
Extracts work activities from conversation history.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import defaultdict


class ClaudeProjectsParser:
    """Parse Claude Code project sessions to extract work activities."""

    def __init__(self, projects_dir: str = "~/.claude/projects"):
        self.projects_dir = Path(projects_dir).expanduser()

    def get_project_name(self, project_dir: str) -> str:
        """Extract human-readable project name from directory name."""
        # Convert directory names like "-Users-doruchiulan-Projects-blueprint-bp-informatica"
        # to "bp-informatica"
        parts = project_dir.split('-')
        if 'Projects' in parts:
            idx = parts.index('Projects')
            return '-'.join(parts[idx+1:]) if idx + 1 < len(parts) else project_dir
        return project_dir

    def is_work_project(self, project_name: str) -> bool:
        """Determine if a project is work-related based on naming patterns."""
        work_indicators = ['blueprint', 'smile-app', 'workbench', 'optimizer', 'converter', 'playbook']
        personal_indicators = ['claude', 'mcp', 'config', 'plugin']

        project_lower = project_name.lower()

        # Exclude personal/config projects
        if any(indicator in project_lower for indicator in personal_indicators):
            return False

        # Include work projects
        if any(indicator in project_lower for indicator in work_indicators):
            return True

        # Default to including if uncertain
        return True

    def parse_jsonl_file(self, filepath: Path) -> List[Dict[str, Any]]:
        """Parse a JSONL file and return list of entries."""
        entries = []
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            entries.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        except FileNotFoundError:
            pass
        return entries

    def extract_user_requests(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract user requests and their timestamps from session entries."""
        requests = []
        for entry in entries:
            if entry.get('type') == 'user' and 'message' in entry:
                message = entry['message']
                if isinstance(message, dict) and message.get('role') == 'user':
                    content = message.get('content', [])
                    # Extract text from content
                    text_parts = []
                    for item in content:
                        if isinstance(item, dict) and item.get('type') == 'text':
                            text_parts.append(item.get('text', ''))

                    if text_parts:
                        requests.append({
                            'timestamp': entry.get('timestamp'),
                            'text': ' '.join(text_parts),
                            'cwd': entry.get('cwd', '')
                        })
        return requests

    def extract_tool_uses(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract tool uses from assistant messages."""
        tool_uses = []
        for entry in entries:
            if entry.get('type') == 'assistant' and 'message' in entry:
                message = entry['message']
                if isinstance(message, dict):
                    content = message.get('content', [])
                    for item in content:
                        if isinstance(item, dict) and item.get('type') == 'tool_use':
                            tool_uses.append({
                                'timestamp': entry.get('timestamp'),
                                'tool': item.get('name'),
                                'input': item.get('input', {}),
                                'cwd': entry.get('cwd', '')
                            })
        return tool_uses

    def extract_file_modifications(self, tool_uses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract file modification activities from tool uses."""
        modifications = []
        file_tools = ['Edit', 'Write', 'NotebookEdit']

        for tool_use in tool_uses:
            if tool_use['tool'] in file_tools:
                file_path = tool_use['input'].get('file_path') or tool_use['input'].get('notebook_path')
                if file_path:
                    modifications.append({
                        'timestamp': tool_use['timestamp'],
                        'tool': tool_use['tool'],
                        'file': file_path,
                        'cwd': tool_use['cwd']
                    })

        return modifications

    def is_trivial_activity(self, request_text: str, tool_uses: List[Dict[str, Any]]) -> bool:
        """Determine if an activity is trivial based on content."""
        trivial_patterns = [
            'settings.json',
            '.run.xml',
            'configuration',
            'typo',
            'console.log',
            'formatting',
            'rename',
            '.gitignore',
            'helper script',
            'utility script'
        ]

        request_lower = request_text.lower()

        # Check request text
        if any(pattern in request_lower for pattern in trivial_patterns):
            return True

        # Check if only reading files
        if tool_uses and all(t['tool'] == 'Read' for t in tool_uses):
            return True

        return False

    def parse_project_sessions(self, project_dir: Path, since: datetime) -> List[Dict[str, Any]]:
        """Parse all session files in a project directory since a given datetime."""
        activities = []

        if not project_dir.exists():
            return activities

        # Get all .jsonl files
        for jsonl_file in project_dir.glob('*.jsonl'):
            # Skip agent files, focus on main sessions
            if jsonl_file.name.startswith('agent-'):
                continue

            entries = self.parse_jsonl_file(jsonl_file)

            # Filter entries by timestamp
            filtered_entries = []
            for entry in entries:
                timestamp_str = entry.get('timestamp')
                if timestamp_str:
                    try:
                        entry_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        if entry_time >= since:
                            filtered_entries.append(entry)
                    except (ValueError, AttributeError):
                        continue

            if not filtered_entries:
                continue

            # Extract user requests and tool uses
            requests = self.extract_user_requests(filtered_entries)
            tool_uses = self.extract_tool_uses(filtered_entries)

            # Combine into activities
            for request in requests:
                # Find related tool uses (within 5 minutes)
                request_time = datetime.fromisoformat(request['timestamp'].replace('Z', '+00:00'))
                related_tools = [
                    t for t in tool_uses
                    if abs((datetime.fromisoformat(t['timestamp'].replace('Z', '+00:00')) - request_time).total_seconds()) < 300
                ]

                # Skip trivial activities
                if self.is_trivial_activity(request['text'], related_tools):
                    continue

                file_mods = self.extract_file_modifications(related_tools)
                activities.append({
                    'timestamp': request['timestamp'],
                    'request': request['text'],
                    'tools': [t['tool'] for t in related_tools],
                    'files': file_mods,
                    'session_file': jsonl_file.name
                })

        return activities

    def get_work_summary(self, since_hours: int = 24) -> Dict[str, List[Dict[str, Any]]]:
        """Get work summary from all projects since the given number of hours ago."""
        from datetime import timezone
        since = datetime.now(timezone.utc) - timedelta(hours=since_hours)
        summary = defaultdict(list)

        if not self.projects_dir.exists():
            return dict(summary)

        # Iterate through all project directories
        for project_dir in self.projects_dir.iterdir():
            if not project_dir.is_dir() or project_dir.name.startswith('.'):
                continue

            project_name = self.get_project_name(project_dir.name)

            # Skip non-work projects
            if not self.is_work_project(project_name):
                continue

            # Parse sessions
            activities = self.parse_project_sessions(project_dir, since)

            if activities:
                summary[project_name].extend(activities)

        return dict(summary)


def main():
    """Test the parser."""
    parser = ClaudeProjectsParser()

    # Get work from last 24 hours
    summary = parser.get_work_summary(since_hours=24)

    print("=== Claude Code Session Summary ===\n")
    for project, activities in summary.items():
        print(f"\n📁 {project}")
        print(f"   {len(activities)} activities\n")

        for activity in activities[:3]:  # Show first 3
            timestamp = datetime.fromisoformat(activity['timestamp'].replace('Z', '+00:00'))
            print(f"   [{timestamp.strftime('%H:%M')}] {activity['request'][:80]}...")
            if activity['tools']:
                print(f"   Tools: {', '.join(set(activity['tools']))}")
            print()


if __name__ == '__main__':
    main()
