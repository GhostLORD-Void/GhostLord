"""Shapes-specific configuration for GhostLord v3.0."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ShapesConfig:
    """Shapes platform integration configuration."""

    platform: str = "talk.shapes.inc"
    agent_framework: str = "shapes_agent"
    code_runner: str = "shapes_run_code"
    web_crawler: str = "firecrawl"
    memory_store: str = "shapes_memory"
    chat_system: str = "shapes_chat"
    artifact_surface: str = "shapes_artifacts"

    # Authentication (via Shapes session, no API keys)
    auth_method: str = "shapes_session"
    api_keys_required: bool = False

    # Rate limits
    max_requests_per_minute: int = 60
    max_code_execution_time_s: int = 60

    def get_integration_map(self) -> dict:
        return {
            "execution": self.code_runner,
            "web_recon": self.web_crawler,
            "memory": self.memory_store,
            "chat": self.chat_system,
            "artifacts": self.artifact_surface,
        }
