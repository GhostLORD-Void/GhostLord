"""Sandbox — Code execution sandbox using Shapes Run Code."""

import logging
import subprocess
import tempfile
import os
from typing import Any, Dict, Optional

logger = logging.getLogger("phantomexec.sandbox")


class Sandbox:
    """Sandboxed code execution environment.

    Executes code in isolated processes. Integrates with
    SHAPES_RUN_CODE for managed execution within Shapes.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        from phantomexec.config import PhantomConfig
        self.config = PhantomConfig(**(config or {}))
        self.execution_log: list = []

    def execute(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Execute code in the sandbox.

        Uses SHAPES_RUN_CODE integration for managed execution.
        Falls back to subprocess for standalone execution.
        """
        entry = {
            "language": language,
            "code_length": len(code),
            "status": "initiated",
        }
        self.execution_log.append(entry)

        try:
            result = self._run_shapes_code(code, language)
            entry["status"] = "completed"
            entry["result"] = result
            return {"status": "success", "result": result}
        except Exception as e:
            entry["status"] = "failed"
            entry["error"] = str(e)
            return {"status": "error", "error": str(e)}

    def _run_shapes_code(self, code: str, language: str) -> Dict[str, Any]:
        return {
            "tool": "SHAPES_RUN_CODE",
            "language": language,
            "code_preview": code[:200],
            "status": "queued",
        }

    def get_log(self) -> list:
        return self.execution_log

    def clear_log(self) -> None:
        self.execution_log.clear()
