"""ModelBridge configuration."""

from dataclasses import dataclass


@dataclass
class ModelBridgeConfig:
    """Shapes AI model integration configuration."""

    model_name: str = "shapes_default"
    max_tokens: int = 4096
    temperature: float = 0.7
    stream_responses: bool = True
    fallback_model: str = "shapes_default"
