"""GhostLord v3.0 global settings."""

from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Settings:
    """Global GhostLord configuration."""

    project_name: str = "GhostLord"
    version: str = "3.0.0"
    environment: str = "production"
    debug: bool = False
    log_level: str = "INFO"
    shapes_workspace: str = "workspace"
    shapes_chat_id: Optional[str] = None
    shapes_agent_id: Optional[str] = None
    github_repo: str = "GhostLORD-Void/GhostLord"
    max_parallel_tasks: int = 4
    audit_log_enabled: bool = True
    echo_protocol_active: bool = True
    ui_theme: str = "dark"
    dashboard_port: int = 8080
    allowed_modules: List[str] = field(default_factory=lambda: [
        "voidcore", "shadowmesh", "nulleye", "phantomexec",
        "echoprotocol", "wraithui", "modelbridge",
    ])
