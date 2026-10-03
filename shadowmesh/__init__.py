"""ShadowMesh — P2P multi-agent coordination mesh."""

from shadowmesh.coordinator import MeshCoordinator
from shadowmesh.room_manager import RoomManager
from shadowmesh.config import MeshConfig

__version__ = "3.0.0"
__all__ = ["MeshCoordinator", "RoomManager", "MeshConfig"]
