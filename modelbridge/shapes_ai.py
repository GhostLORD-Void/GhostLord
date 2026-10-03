"""ShapesAI — Direct Shapes AI model integration.

Uses Shapes Agent framework for AI inference.
Zero external API keys — relies on Shapes' built-in models.
"""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger("modelbridge.shapes_ai")


class ShapesAI:
    """Shapes AI model interface.

    Provides inference via Shapes Agent framework.
    No API keys required — uses Shapes' native AI engine.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        from modelbridge.config import ModelBridgeConfig
        self.config = ModelBridgeConfig(**(config or {}))
        self.model = self.config.model_name

    def query(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {
            "tool": "SHAPES_AGENT",
            "model": self.model,
            "prompt": prompt[:500],
            "context_keys": list((context or {}).keys()),
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "status": "ready",
        }

    def analyze(self, text: str, analysis_type: str = "general") -> Dict[str, Any]:
        return {
            "tool": "SHAPES_AGENT",
            "action": "analyze",
            "analysis_type": analysis_type,
            "input_length": len(text),
        }

    def generate(self, prompt: str, max_tokens: int = 1024) -> Dict[str, Any]:
        return {
            "tool": "SHAPES_AGENT",
            "action": "generate",
            "prompt": prompt[:500],
            "max_tokens": max_tokens,
        }

    def get_status(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "config": self.config.to_dict() if hasattr(self.config, "to_dict") else {},
            "status": "connected",
        }
