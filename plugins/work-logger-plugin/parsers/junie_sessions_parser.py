#!/usr/bin/env python3
"""
Parser for Junie (Matterhorn) sessions stored in JetBrains caches.
Extracts work activities from Junie conversation history.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import defaultdict


class JunieSessionsParser:
    """Parse Junie/Matterhorn sessions to extract work activities."""

    def __init__(self, jetbrains_cache_dir: str = "~/Library/Caches/JetBrains"):
        self.cache_dir = Path(jetbrains_cache_dir).expanduser()

    def find_matterhorn_directories(self) -> List[Path]:
        """Find all .matterhorn directories across all IntelliJ versions."""
        matterhorn_dirs = []

        if not self.cache_dir.exists():
            return matterhorn_dirs

        # Search in IntelliJIdea* directories
        for intellij_dir in self.cache_dir.glob("IntelliJIdea*/projects/*"):
            matterhorn_path = intellij_dir / "matterhorn" / ".matterhorn"
            if matterhorn_path.exists():
                matterhorn_dirs.append(matterhorn_path)

        return matterhorn_dirs

    def extract_project_from_path(self, matterhorn_path: Path) -> str:
        """Extract project name from matterhorn path."""
        # Path format: .../projects/{project}.{hash}/matterhorn/.matterhorn
        parts = matterhorn_path.parts

        try:
            projects_idx = parts.index("projects")
            if projects_idx + 1 < len(parts):
                project_part = parts[projects_idx + 1]
                # Remove hash suffix: "smile-app.9b05b6ff" -> "smile-app"
                project_name = project_part.split('.')[0]
                return project_name
        except (ValueError, IndexError):
            pass

        return "unknown"

    def is_work_project(self, project_name: str) -> bool:
        """Determine if a project is work-related based on naming patterns."""
        work_indicators = ['blueprint', 'smile-app', 'workbench', 'optimizer', 'converter', 'playbook', 'dbricks']
        personal_indicators = ['claude', 'mcp', 'config', 'plugin', 'dotfiles', 'test', 'demo']

        project_lower = project_name.lower()

        # Exclude personal/config projects
        if any(indicator in project_lower for indicator in personal_indicators):
            return False

        # Include work projects
        if any(indicator in project_lower for indicator in work_indicators):
            return True

        # Default to including if uncertain
        return True

    def parse_chain_metadata(self, chain_file: Path) -> Optional[Dict[str, Any]]:
        """Parse chain metadata JSON file."""
        try:
            with open(chain_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def parse_task_file(self, task_file: Path) -> Optional[Dict[str, Any]]:
        """Parse task JSON file."""
        try:
            with open(task_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def extract_user_messages(self, task_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract user messages and responses from task data."""
        messages = []

        # Get initial context/description
        context = task_data.get('context', {})
        description = context.get('description', '')

        if description and len(description) > 5:
            created = task_data.get('created')
            messages.append({
                'timestamp': created,
                'type': 'user_request',
                'text': description
            })

        # Extract from observations
        observations = task_data.get('finalAgentState', {}).get('observations', [])

        for obs in observations:
            # User responses
            user_response = obs.get('userResponse', {})
            if user_response:
                user_type = user_response.get('type', '')

                # Check for text messages
                if 'MatterhornUserChatMessage' in user_type:
                    content = user_response.get('content', '')
                    if content and len(content) > 5:
                        messages.append({
                            'timestamp': obs.get('created'),
                            'type': 'user_response',
                            'text': content
                        })

            # Assistant requests (to understand what was asked/discussed)
            assistant_request = obs.get('assistantRequest', {})
            if assistant_request:
                content = assistant_request.get('content', '')

                # Extract plan and actions from UPDATE tags
                if '<PLAN>' in content and '</PLAN>' in content:
                    plan_start = content.index('<PLAN>') + 6
                    plan_end = content.index('</PLAN>')
                    plan_text = content[plan_start:plan_end].strip()

                    if plan_text:
                        messages.append({
                            'timestamp': obs.get('created'),
                            'type': 'assistant_plan',
                            'text': plan_text
                        })

                if '<NEXT_STEP>' in content and '</NEXT_STEP>' in content:
                    step_start = content.index('<NEXT_STEP>') + 11
                    step_end = content.index('</NEXT_STEP>')
                    step_text = content[step_start:step_end].strip()

                    if step_text:
                        messages.append({
                            'timestamp': obs.get('created'),
                            'type': 'assistant_action',
                            'text': step_text
                        })

        return messages

    def extract_tool_uses(self, task_data: Dict[str, Any]) -> List[str]:
        """Extract tools used from task data."""
        tools = set()

        observations = task_data.get('finalAgentState', {}).get('observations', [])

        for obs in observations:
            assistant_request = obs.get('assistantRequest', {})
            tool_uses = assistant_request.get('toolUses', [])

            for tool_use in tool_uses:
                tool_name = tool_use.get('name')
                if tool_name:
                    tools.add(tool_name)

        return list(tools)

    def extract_files_from_context(self, task_data: Dict[str, Any]) -> List[str]:
        """Extract files from editor context."""
        files = []

        editor_context = task_data.get('finalAgentState', {}).get('issue', {}).get('editorContext', {})

        # Get open files
        open_files = editor_context.get('openFiles', [])
        files.extend(open_files[:5])  # Limit to first 5

        return files

    def is_trivial_activity(self, description: str) -> bool:
        """Determine if an activity is trivial based on content."""
        trivial_patterns = [
            'formatting',
            'typo',
            'whitespace',
            'indentation',
            'rename variable',
            'console.log',
            '.gitignore',
            'configuration',
            'settings.json'
        ]

        description_lower = description.lower()
        return any(pattern in description_lower for pattern in trivial_patterns)

    def parse_chains_in_directory(self, matterhorn_dir: Path, since: datetime) -> List[Dict[str, Any]]:
        """Parse all chains (conversation threads) in a matterhorn directory."""
        activities = []
        issues_dir = matterhorn_dir / "issues"

        if not issues_dir.exists():
            return activities

        # Iterate through all chain JSON files
        for chain_file in issues_dir.glob("chain-*.json"):
            chain_metadata = self.parse_chain_metadata(chain_file)

            if not chain_metadata:
                continue

            # Check timestamp
            created_str = chain_metadata.get('created')
            if not created_str:
                continue

            try:
                created_time = datetime.fromisoformat(created_str.replace('Z', '+00:00'))
                if created_time < since:
                    continue
            except (ValueError, AttributeError):
                continue

            chain_name = chain_metadata.get('name', 'Unnamed task')
            chain_id = chain_metadata['id']['id']

            # Skip trivial activities
            if self.is_trivial_activity(chain_name):
                continue

            # Parse task files in this chain
            chain_dir = issues_dir / f"chain-{chain_id}"

            if not chain_dir.exists():
                continue

            for task_file in chain_dir.glob("task-*.json"):
                task_data = self.parse_task_file(task_file)

                if not task_data:
                    continue

                # Extract messages and tools
                messages = self.extract_user_messages(task_data)
                tools = self.extract_tool_uses(task_data)
                files = self.extract_files_from_context(task_data)

                # Combine relevant messages into summary
                summary_parts = [chain_name]

                # Add key user messages
                user_msgs = [m['text'] for m in messages if m['type'] == 'user_request' or m['type'] == 'user_response']
                if user_msgs:
                    summary_parts.append(user_msgs[0][:100])  # First user message

                activities.append({
                    'timestamp': created_str,
                    'request': ' - '.join(summary_parts),
                    'tools': tools,
                    'files': files,
                    'chain_name': chain_name,
                    'state': chain_metadata.get('state', 'Unknown')
                })

        return activities

    def get_work_summary(self, since_hours: int = 24) -> Dict[str, List[Dict[str, Any]]]:
        """Get work summary from all Junie sessions since the given number of hours ago."""
        from datetime import timezone
        since = datetime.now(timezone.utc) - timedelta(hours=since_hours)
        summary = defaultdict(list)

        # Find all matterhorn directories
        matterhorn_dirs = self.find_matterhorn_directories()

        for matterhorn_dir in matterhorn_dirs:
            project_name = self.extract_project_from_path(matterhorn_dir)

            # Skip non-work projects
            if not self.is_work_project(project_name):
                continue

            # Parse chains/sessions
            activities = self.parse_chains_in_directory(matterhorn_dir, since)

            if activities:
                summary[project_name].extend(activities)

        return dict(summary)


def main():
    """Test the parser."""
    parser = JunieSessionsParser()

    # Get work from last 24 hours
    summary = parser.get_work_summary(since_hours=24)

    print("=== Junie (Matterhorn) Session Summary ===\n")

    if not summary:
        print("No Junie work activities found in the last 24 hours.")
        return

    for project, activities in summary.items():
        print(f"\n📁 {project}")
        print(f"   {len(activities)} activities\n")

        for activity in activities[:5]:  # Show first 5
            timestamp = datetime.fromisoformat(activity['timestamp'].replace('Z', '+00:00'))
            print(f"   [{timestamp.strftime('%H:%M')}] {activity['chain_name']}")
            print(f"   Request: {activity['request'][:100]}...")
            if activity['tools']:
                print(f"   Tools: {', '.join(activity['tools'])}")
            print(f"   State: {activity['state']}")
            print()


if __name__ == '__main__':
    main()
