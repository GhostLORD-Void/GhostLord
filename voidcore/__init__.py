"""VoidCore — Autonomous task orchestration engine for GhostLord v3.0."""

from voidcore.orchestrator import Orchestrator
from voidcore.shapes_bridge import ShapesBridge
from voidcore.config import CoreConfig

__version__ = "3.0.0"
__all__ = ["Orchestrator", "ShapesBridge", "CoreConfig"]
