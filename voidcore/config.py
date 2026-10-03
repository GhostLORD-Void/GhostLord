"""VoidCore configuration — Shapes-native settings."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CoreConfig:
    """GhostLord v3.0 core configuration."""

    agent_name: str = "GhostLord"
    version: str = "3.0.0"
    shapes_workspace: str = "workspace"
    shapes_chat_id: Optional[str] = None
    shapes_agent_id: Optional[str] = None
    log_level: str = "INFO"
    max_parallel_tasks: int = 4
    audit_enabled: bool = True
    echo_protocol_active: bool = True
    model_preference: str = "shapes_default"

    def get_shapes_session(self) -> dict:
        return {
            "workspace": self.shapes_workspace,
            "agent_id": self.shapes_agent_id,
            "chat_id": self.shapes_chat_id,
        }

    def to_dict(self) -> dict:
        return {
            "agent_name": self.agent_name,
            "version": self.version,
            "log_level": self.log_level,
            "max_parallel_tasks": self.max_parallel_tasks,
            "audit_enabled": self.audit_enabled,
            "model_preference": self.model_preference,
        }
