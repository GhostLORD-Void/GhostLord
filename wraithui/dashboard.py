"""Dashboard — Web dashboard via SHAPES_CREATE_FILE artifacts."""

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger("wraithui.dashboard")


class Dashboard:
    """Web dashboard generator using Shapes artifact surface.

    Creates interactive HTML dashboards via SHAPES_CREATE_FILE.
    Displays agent status, task metrics, and audit trail.
    """

    def __init__(self):
        self.metrics: Dict[str, Any] = {}
        self.tasks: List[Dict[str, Any]] = []

    def update_metric(self, key: str, value: Any) -> None:
        self.metrics[key] = value

    def add_task(self, task: Dict[str, Any]) -> None:
        task["added_at"] = datetime.now(timezone.utc).isoformat()
        self.tasks.append(task)

    def render_html(self) -> str:
        html = f"""<!DOCTYPE html>
<html>
<head><title>GhostLord v3.0 Dashboard</title>
<style>
body {{ font-family: monospace; background: #0a0a0a; color: #00ff88; padding: 20px; }}
h1 {{ color: #ff0040; }}
.metric {{ margin: 10px 0; padding: 8px; border: 1px solid #333; }}
.task {{ margin: 5px 0; padding: 5px; background: #111; }}
</style></head>
<body>
<h1>GhostLord v3.0 Dashboard</h1>
<p>Generated: {datetime.now(timezone.utc).isoformat()}</p>
<div id="metrics">
"""
        for key, value in self.metrics.items():
            html += f'<div class="metric"><strong>{key}</strong>: {value}</div>\n'
        html += '</div>\n<div id="tasks">\n'
        for task in self.tasks[-10:]:
            html += f'<div class="task">{task.get("type", "unknown")} - {task.get("status", "pending")}</div>\n'
        html += '</div>\n</body>\n</html>'
        return html

    def save_artifact(self, filename: str = "ghostlord_dashboard.html") -> Dict[str, Any]:
        return {
            "tool": "SHAPES_CREATE_FILE",
            "filename": filename,
            "mime_type": "text/html",
            "content_length": len(self.render_html()),
            "status": "ready",
        }

    def get_status(self) -> Dict[str, Any]:
        return {
            "dashboard_active": True,
            "total_tasks": len(self.tasks),
            "metrics_count": len(self.metrics),
        }
