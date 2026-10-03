"""VoidCore orchestrator — main task execution engine."""

import importlib
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger("voidcore.orchestrator")


class Orchestrator:
    """Autonomous task orchestration engine.

    Coordinates all GhostLord modules through Shapes-native tool integration.
    No external API keys — uses SHAPES_RUN_CODE, SHAPES_WEB_CRAWL,
    SHAPES_CHAT_ACTIONS, SHAPES_TOTAL_RECALL_BROWSE, SHAPES_CREATE_FILE.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        from voidcore.config import CoreConfig
        from voidcore.shapes_bridge import ShapesBridge
        from echoprotocol.audit import AuditLogger
        from modelbridge.shapes_ai import ShapesAI

        self.config = CoreConfig(**(config or {}))
        self.bridge = ShapesBridge(self.config)
        self.audit = AuditLogger()
        self.ai = ShapesAI()
        self._modules: Dict[str, Any] = {}
        self._task_counter = 0

    def register_module(self, name: str, module: Any) -> None:
        self._modules[name] = module
        logger.info("Module registered: %s", name)

    def execute_task(self, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        self._task_counter += 1
        task_id = f"task_{self._task_counter:04d}"
        start = datetime.utcnow()

        self.audit.log_action("TASK_START", {"task_id": task_id, "type": task_type})

        try:
            if task_type == "recon":
                result = self._execute_recon(payload)
            elif task_type == "execute":
                result = self._execute_code(payload)
            elif task_type == "chat":
                result = self._execute_chat(payload)
            elif task_type == "crawl":
                result = self._execute_crawl(payload)
            elif task_type == "memory":
                result = self._execute_memory(payload)
            else:
                result = self._execute_generic(payload)

            duration = (datetime.utcnow() - start).total_seconds()
            self.audit.log_action("TASK_COMPLETE", {"task_id": task_id, "duration_s": duration})
            return {"task_id": task_id, "status": "success", "result": result, "duration_s": duration}

        except Exception as e:
            duration = (datetime.utcnow() - start).total_seconds()
            self.audit.log_action("TASK_ERROR", {"task_id": task_id, "error": str(e)})
            return {"task_id": task_id, "status": "error", "error": str(e), "duration_s": duration}

    def run(self, task_type: str = "generic", payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a single task — main entry point for autonomous execution."""
        return self.execute_task(task_type, payload or {})

    def _execute_recon(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        from nulleye.recon import ReconEngine
        engine = ReconEngine()
        return engine.run(payload)

    def _execute_code(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        from phantomexec.sandbox import Sandbox
        sandbox = Sandbox()
        return sandbox.execute(payload.get("code", ""))

    def _execute_chat(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        from shadowmesh.coordinator import MeshCoordinator
        coordinator = MeshCoordinator()
        return coordinator.send(payload)

    def _execute_crawl(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        from nulleye.recon import Crawler
        crawler = Crawler()
        return crawler.crawl(payload.get("url", ""))

    def _execute_memory(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        from echoprotocol.audit import AuditLogger
        logger = AuditLogger()
        return logger.query(payload.get("query", ""))

    def _execute_generic(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"message": "Generic task executed", "payload_keys": list(payload.keys())}

    def run_autonomous_loop(self, iterations: int = 10) -> List[Dict[str, Any]]:
        results = []
        for i in range(iterations):
            result = self.execute_task("generic", {"iteration": i})
            results.append(result)
        return results
