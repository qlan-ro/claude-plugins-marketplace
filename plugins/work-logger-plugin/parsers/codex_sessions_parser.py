#!/usr/bin/env python3
"""
Parser for Codex sessions stored in ~/.codex/sessions/
Extracts work activities from Codex conversation history.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional
from collections import defaultdict


class CodexSessionsParser:
    """Parse Codex sessions to extract work activities."""

    def __init__(self, sessions_dir: str = "~/.codex/sessions"):
        self.sessions_dir = Path(sessions_dir).expanduser()

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

    def extract_project_from_cwd(self, cwd: str) -> str:
        """Extract project name from working directory."""
        if not cwd:
            return "unknown"

        path_parts = Path(cwd).parts
        if 'Projects' in path_parts:
            idx = path_parts.index('Projects')
            if idx + 1 < len(path_parts):
                # Return the immediate subdirectory after Projects
                return path_parts[idx + 1]

        # Fallback to last directory
        return path_parts[-1] if path_parts else "unknown"

    def is_work_project(self, project_name: str) -> bool:
        """Determine if a project is work-related based on naming patterns."""
        work_indicators = ['blueprint', 'smile-app', 'workbench', 'optimizer', 'converter', 'playbook']
        personal_indicators = ['claude', 'mcp', 'config', 'plugin', 'dotfiles']

        project_lower = project_name.lower()

        # Exclude personal/config projects
        if any(indicator in project_lower for indicator in personal_indicators):
            return False

        # Include work projects
        if any(indicator in project_lower for indicator in work_indicators):
            return True

        # Default to including if uncertain
        return True

    def extract_user_messages(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract user messages from session entries."""
        messages = []

        for entry in entries:
            if entry.get('type') == 'event_msg':
                payload = entry.get('payload', {})
                if payload.get('type') == 'user_message':
                    message_text = payload.get('message', '')
                    timestamp = entry.get('timestamp')

                    # Skip IDE context messages
                    if message_text.startswith('# Context from my IDE setup:'):
                        # Extract actual user request
                        if '## My request for Codex:' in message_text:
                            request = message_text.split('## My request for Codex:')[1].strip()
                            messages.append({
                                'timestamp': timestamp,
                                'text': request
                            })
                    else:
                        messages.append({
                            'timestamp': timestamp,
                            'text': message_text
                        })

        return messages

    def extract_tool_uses(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract tool/function calls from session entries."""
        tool_uses = []

        for entry in entries:
            if entry.get('type') == 'response_item':
                payload = entry.get('payload', {})

                # Check for function calls
                if payload.get('type') == 'function_call':
                    tool_name = payload.get('name')
                    arguments = payload.get('arguments', '{}')

                    try:
                        args_dict = json.loads(arguments) if isinstance(arguments, str) else arguments
                    except json.JSONDecodeError:
                        args_dict = {}

                    tool_uses.append({
                        'timestamp': entry.get('timestamp'),
                        'tool': tool_name,
                        'input': args_dict
                    })

        return tool_uses

    def extract_file_operations(self, tool_uses: List[Dict[str, Any]]) -> List[str]:
        """Extract file paths from tool uses."""
        files = []
        file_tools = ['write_file', 'read_file', 'edit_file', 'shell_command']

        for tool_use in tool_uses:
            if tool_use['tool'] in file_tools:
                input_data = tool_use['input']

                # Extract file paths from various input formats
                if 'path' in input_data:
                    files.append(input_data['path'])
                elif 'file_path' in input_data:
                    files.append(input_data['file_path'])
                elif tool_use['tool'] == 'shell_command' and 'command' in input_data:
                    # Try to extract files from command
                    command = input_data['command']
                    # Simple heuristic: look for file patterns
                    if any(ext in command for ext in ['.py', '.java', '.ts', '.json', '.xml']):
                        files.append(f"<from command: {command[:50]}...>")

        return files

    def is_trivial_activity(self, message_text: str, tool_uses: List[Dict[str, Any]]) -> bool:
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
            'utility script',
            'ls -la',
            'cd ',
            'pwd'
        ]

        message_lower = message_text.lower()

        # Check message text
        if any(pattern in message_lower for pattern in trivial_patterns):
            return True

        # Check if only reading or listing
        if tool_uses:
            tool_names = [t['tool'] for t in tool_uses]
            if all(name in ['read_file', 'shell_command'] for name in tool_names):
                # Check if shell commands are just ls/cd/pwd
                commands = [
                    t['input'].get('command', '') for t in tool_uses
                    if t['tool'] == 'shell_command'
                ]
                if commands and all(
                    cmd.startswith(('ls', 'cd', 'pwd', 'cat'))
                    for cmd in commands
                ):
                    return True

        return False

    def parse_session_file(self, session_file: Path, since: datetime) -> List[Dict[str, Any]]:
        """Parse a single session file and extract activities."""
        activities = []
        entries = self.parse_jsonl_file(session_file)

        if not entries:
            return activities

        # Filter by timestamp
        filtered_entries = [
            e for e in entries
            if e.get('timestamp') and
            datetime.fromisoformat(e['timestamp'].replace('Z', '+00:00')) >= since
        ]

        if not filtered_entries:
            return activities

        # Get working directory from session metadata
        cwd = None
        for entry in filtered_entries:
            if entry.get('type') == 'session_meta':
                payload = entry.get('payload', {})
                cwd = payload.get('cwd')
                break

        project = self.extract_project_from_cwd(cwd) if cwd else "unknown"

        # Extract messages and tool uses
        messages = self.extract_user_messages(filtered_entries)
        tool_uses = self.extract_tool_uses(filtered_entries)

        # Combine into activities
        for message in messages:
            msg_time = datetime.fromisoformat(message['timestamp'].replace('Z', '+00:00'))

            # Find related tool uses (within 5 minutes)
            related_tools = [
                t for t in tool_uses
                if abs((datetime.fromisoformat(t['timestamp'].replace('Z', '+00:00')) - msg_time).total_seconds()) < 300
            ]

            # Skip trivial activities
            if self.is_trivial_activity(message['text'], related_tools):
                continue

            # Skip empty or very short messages
            if len(message['text'].strip()) < 5:
                continue

            files = self.extract_file_operations(related_tools)

            activities.append({
                'timestamp': message['timestamp'],
                'request': message['text'],
                'tools': [t['tool'] for t in related_tools],
                'files': files,
                'project': project,
                'cwd': cwd,
                'session_file': session_file.name
            })

        return activities

    def get_sessions_for_date(self, target_date: date) -> List[Path]:
        """Get all session files for a specific date."""
        year = target_date.year
        month = target_date.month
        day = target_date.day

        session_dir = self.sessions_dir / str(year) / f"{month:02d}" / f"{day:02d}"

        if not session_dir.exists():
            return []

        return list(session_dir.glob("rollout-*.jsonl"))

    def get_work_summary(self, since_hours: int = 24) -> Dict[str, List[Dict[str, Any]]]:
        """Get work summary from all sessions since the given number of hours ago."""
        from datetime import timezone
        since = datetime.now(timezone.utc) - timedelta(hours=since_hours)
        summary = defaultdict(list)

        # Calculate date range to check
        days_to_check = (since_hours // 24) + 2  # Add buffer
        dates_to_check = [
            date.today() - timedelta(days=i)
            for i in range(days_to_check)
        ]

        for check_date in dates_to_check:
            session_files = self.get_sessions_for_date(check_date)

            for session_file in session_files:
                activities = self.parse_session_file(session_file, since)

                for activity in activities:
                    project = activity['project']

                    # Skip non-work projects
                    if not self.is_work_project(project):
                        continue

                    if project not in summary:
                        summary[project] = []

                    summary[project].append(activity)

        return dict(summary)


def main():
    """Test the parser."""
    parser = CodexSessionsParser()

    # Get work from last 24 hours
    summary = parser.get_work_summary(since_hours=24)

    print("=== Codex Session Summary ===\n")

    if not summary:
        print("No work activities found in the last 24 hours.")
        return

    for project, activities in summary.items():
        print(f"\n📁 {project}")
        print(f"   {len(activities)} activities\n")

        for activity in activities[:3]:  # Show first 3
            timestamp = datetime.fromisoformat(activity['timestamp'].replace('Z', '+00:00'))
            print(f"   [{timestamp.strftime('%H:%M')}] {activity['request'][:80]}...")
            if activity['tools']:
                print(f"   Tools: {', '.join(set(activity['tools']))}")
            if activity['files']:
                print(f"   Files: {len(activity['files'])} modified")
            print()


if __name__ == '__main__':
    main()
