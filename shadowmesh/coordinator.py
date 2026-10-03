"""MeshCoordinator — Multi-agent task coordination via Shapes Chat."""

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger("shadowmesh.coordinator")


class MeshCoordinator:
    """Coordinates multiple GhostLord agents through Shapes chat rooms.

    Uses SHAPES_CHAT_ACTIONS for room creation, messaging, and agent
    coordination. Each task gets a dedicated Shapes chat room.
    """

    def __init__(self):
        from shadowmesh.config import MeshConfig
        self.config = MeshConfig()
        self.active_rooms: Dict[str, Dict[str, Any]] = {}

    def create_task_room(self, task_id: str, participants: Optional[List[str]] = None) -> Dict[str, Any]:
        room_name = self.config.get_room_name(task_id)
        self.active_rooms[task_id] = {
            "room_name": room_name,
            "participants": participants or [],
            "created_at": datetime.utcnow().isoformat(),
            "status": "active",
        }
        logger.info("Task room created: %s", room_name)
        return {"task_id": task_id, "room_name": room_name, "status": "created"}

    def assign_agent(self, task_id: str, agent_name: str) -> Dict[str, Any]:
        if task_id not in self.active_rooms:
            return {"error": f"Task room {task_id} not found"}
        room = self.active_rooms[task_id]
        room["participants"].append(agent_name)
        return {"task_id": task_id, "agent": agent_name, "status": "assigned"}

    def broadcast(self, task_id: str, message: str) -> Dict[str, Any]:
        if task_id not in self.active_rooms:
            return {"error": f"Task room {task_id} not found"}
        return {
            "task_id": task_id,
            "action": "broadcast",
            "message": message[:500],
            "recipients": len(self.active_rooms[task_id]["participants"]),
        }

    def get_room_status(self, task_id: str) -> Dict[str, Any]:
        room = self.active_rooms.get(task_id)
        if not room:
            return {"error": "Room not found"}
        return room

    def list_rooms(self) -> List[Dict[str, Any]]:
        return list(self.active_rooms.values())
