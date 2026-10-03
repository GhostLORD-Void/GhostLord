"""ShadowMesh configuration."""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class MeshConfig:
    """Multi-agent mesh network configuration."""

    mesh_name: str = "GhostLordMesh"
    max_agents: int = 10
    room_prefix: str = "ghostlord-"
    encryption: bool = True
    protocol: str = "shapes_chat"
    heartbeat_interval_s: int = 30
    agent_list: List[str] = field(default_factory=list)

    def get_room_name(self, task_id: str) -> str:
        return f"{self.room_prefix}{task_id}"
