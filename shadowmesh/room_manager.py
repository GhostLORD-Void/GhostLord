"""RoomManager — Shapes chat room lifecycle management."""

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger("shadowmesh.room_manager")


class RoomManager:
    """Manages Shapes chat rooms for GhostLord multi-agent operations.

    Uses SHAPES_CHAT_ACTIONS to create, manage, and close chat rooms.
    Each room serves as a coordination channel for a specific task.
    """

    def __init__(self):
        self.rooms: Dict[str, Dict[str, Any]] = {}

    def create_room(self, title: str, invite_link: Optional[str] = None) -> Dict[str, Any]:
        room_id = f"room_{len(self.rooms) + 1:04d}"
        self.rooms[room_id] = {
            "title": title,
            "created_at": datetime.utcnow().isoformat(),
            "invite_link": invite_link,
            "status": "active",
            "message_count": 0,
        }
        logger.info("Room created: %s -> %s", room_id, title)
        return {"room_id": room_id, "title": title, "status": "active"}

    def send_message(self, room_id: str, message: str) -> Dict[str, Any]:
        if room_id not in self.rooms:
            return {"error": "Room not found"}
        self.rooms[room_id]["message_count"] += 1
        return {"room_id": room_id, "message_length": len(message), "msg_number": self.rooms[room_id]["message_count"]}

    def close_room(self, room_id: str) -> Dict[str, Any]:
        if room_id not in self.rooms:
            return {"error": "Room not found"}
        self.rooms[room_id]["status"] = "closed"
        return {"room_id": room_id, "status": "closed"}

    def get_room(self, room_id: str) -> Optional[Dict[str, Any]]:
        return self.rooms.get(room_id)

    def list_active_rooms(self) -> List[str]:
        return [rid for rid, room in self.rooms.items() if room["status"] == "active"]
