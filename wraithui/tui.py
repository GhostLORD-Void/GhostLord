"""GhostLordTUI — Terminal user interface using Rich/Textual."""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger("wraithui.tui")


class GhostLordTUI:
    """Terminal-first TUI for GhostLord v3.0.

    Uses Rich for terminal rendering and Textual for
    interactive widgets. Displays agent status, task
    queue, and audit trail.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        from wraithui.config import UIConfig
        self.config = UIConfig(**(config or {}))
        self.active = False

    def render_banner(self) -> str:
        return """
╔══════════════════════════════════════════════╗
║  GHOSTLORD v3.0 — AUTONOMOUS VOID AGENT      ║
║  Shapes-Native | Zero API Keys | Free        ║
╚══════════════════════════════════════════════╝
"""

    def render_status(self, status: Dict[str, Any]) -> str:
        lines = ["[STATUS]"]
        for key, value in status.items():
            lines.append(f"  {key}: {value}")
        return "\n".join(lines)

    def render_task_queue(self, tasks: list) -> str:
        if not tasks:
            return "  [empty queue]"
        lines = ["[TASK QUEUE]"]
        for i, task in enumerate(tasks):
            lines.append(f"  {i+1}. {task.get('type', 'unknown')} - {task.get('status', 'pending')}")
        return "\n".join(lines)

    def start(self) -> Dict[str, Any]:
        self.active = True
        logger.info("GhostLordTUI started")
        return {"status": "active", "banner": self.render_banner()}

    def stop(self) -> Dict[str, Any]:
        self.active = False
        return {"status": "stopped"}
