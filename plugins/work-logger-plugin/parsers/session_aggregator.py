#!/usr/bin/env python3
"""
Unified session aggregator that combines Claude Code and Codex sessions
to generate comprehensive work summaries.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict

# Add parsers to path
sys.path.insert(0, str(Path(__file__).parent))

from claude_projects_parser import ClaudeProjectsParser
from codex_sessions_parser import CodexSessionsParser
from junie_sessions_parser import JunieSessionsParser


class SessionAggregator:
    """Aggregate work activities from multiple AI assistant session sources."""

    def __init__(self):
        self.claude_parser = ClaudeProjectsParser()
        self.codex_parser = CodexSessionsParser()
        self.junie_parser = JunieSessionsParser()

    def merge_activities(
        self,
        claude_summary: Dict[str, List[Dict[str, Any]]],
        codex_summary: Dict[str, List[Dict[str, Any]]],
        junie_summary: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Merge activities from all sources, removing duplicates."""
        merged = defaultdict(list)

        # Add Claude activities
        for project, activities in claude_summary.items():
            for activity in activities:
                activity['source'] = 'claude'
                merged[project].append(activity)

        # Add Codex activities
        for project, activities in codex_summary.items():
            for activity in activities:
                activity['source'] = 'codex'
                merged[project].append(activity)

        # Add Junie activities
        for project, activities in junie_summary.items():
            for activity in activities:
                activity['source'] = 'junie'
                merged[project].append(activity)

        # Sort activities by timestamp within each project
        for project in merged:
            merged[project].sort(
                key=lambda x: datetime.fromisoformat(x['timestamp'].replace('Z', '+00:00'))
            )

        return dict(merged)

    def get_work_summary(self, since_hours: int = 24) -> Dict[str, List[Dict[str, Any]]]:
        """Get comprehensive work summary from all sources."""
        print(f"Fetching work activities from the last {since_hours} hours...\n", file=sys.stderr)

        # Get summaries from all sources
        claude_summary = self.claude_parser.get_work_summary(since_hours)
        codex_summary = self.codex_parser.get_work_summary(since_hours)
        junie_summary = self.junie_parser.get_work_summary(since_hours)

        print(f"Claude Code sessions: {sum(len(v) for v in claude_summary.values())} activities", file=sys.stderr)
        print(f"Codex sessions: {sum(len(v) for v in codex_summary.values())} activities", file=sys.stderr)
        print(f"Junie sessions: {sum(len(v) for v in junie_summary.values())} activities\n", file=sys.stderr)

        # Merge and return
        return self.merge_activities(claude_summary, codex_summary, junie_summary)

    def format_for_logging(self, summary: Dict[str, List[Dict[str, Any]]]) -> str:
        """Format summary in a log-friendly format."""
        lines = []

        for project, activities in summary.items():
            lines.append(f"\n=== {project} ===\n")

            for activity in activities:
                timestamp = datetime.fromisoformat(activity['timestamp'].replace('Z', '+00:00'))
                time_str = timestamp.strftime('%H:%M')
                source = activity['source'].upper()

                lines.append(f"[{time_str}] [{source}]")
                lines.append(f"Request: {activity['request'][:100]}")

                if activity.get('tools'):
                    lines.append(f"Tools: {', '.join(set(activity['tools']))}")

                if activity.get('files'):
                    files = activity['files']
                    if isinstance(files, list):
                        if len(files) > 0:
                            # Handle both string paths and dict objects
                            file_strs = []
                            for f in files[:5]:  # Limit to first 5
                                if isinstance(f, dict):
                                    file_strs.append(f.get('file', str(f)))
                                else:
                                    file_strs.append(str(f))
                            lines.append(f"Files: {', '.join(file_strs)}")

                lines.append("---\n")

        return '\n'.join(lines)

    def get_activity_summary_bullets(self, summary: Dict[str, List[Dict[str, Any]]]) -> List[str]:
        """Generate bullet-point summary of key activities."""
        bullets = []
        seen_requests = set()

        # Collect all activities across projects
        all_activities = []
        for project, activities in summary.items():
            for activity in activities:
                activity['project'] = project
                all_activities.append(activity)

        # Sort by timestamp
        all_activities.sort(
            key=lambda x: datetime.fromisoformat(x['timestamp'].replace('Z', '+00:00')),
            reverse=True
        )

        # Extract key points
        for activity in all_activities:
            request = activity['request'].strip()

            # Skip if we've seen similar request
            request_key = request[:50].lower()
            if request_key in seen_requests:
                continue
            seen_requests.add(request_key)

            # Look for substantial work indicators
            substantial_keywords = [
                'pr', 'pull request', 'merge', 'deploy',
                'implement', 'fix', 'bug', 'feature',
                'api', 'endpoint', 'migration', 'refactor',
                'optimize', 'performance', 'review',
                'sync', 'meeting', 'discuss'
            ]

            request_lower = request.lower()
            if any(keyword in request_lower for keyword in substantial_keywords):
                # Extract relevant portion
                summary_text = request[:150]
                if len(request) > 150:
                    summary_text += "..."

                project = activity.get('project', 'unknown')
                bullets.append(f"{project}: {summary_text}")

                if len(bullets) >= 10:  # Limit to top 10
                    break

        return bullets


def main():
    """Test the aggregator."""
    import argparse

    parser = argparse.ArgumentParser(description='Aggregate AI assistant session data')
    parser.add_argument(
        '--hours',
        type=int,
        default=24,
        help='Number of hours to look back (default: 24)'
    )
    parser.add_argument(
        '--format',
        choices=['log', 'bullets'],
        default='log',
        help='Output format (default: log)'
    )

    args = parser.parse_args()

    aggregator = SessionAggregator()
    summary = aggregator.get_work_summary(since_hours=args.hours)

    if not summary:
        print("No work activities found.")
        return

    if args.format == 'bullets':
        bullets = aggregator.get_activity_summary_bullets(summary)
        print("\n=== Key Activities ===\n")
        for bullet in bullets:
            print(f"• {bullet}")
    else:
        output = aggregator.format_for_logging(summary)
        print(output)


if __name__ == '__main__':
    main()
