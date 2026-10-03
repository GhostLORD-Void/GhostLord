"""EchoProtocol configuration."""

from dataclasses import dataclass


@dataclass
class EchoConfig:
    """Self-audit configuration."""

    log_file: str = "ghostlord_audit.log"
    hash_algorithm: str = "sha256"
    chain_enabled: bool = True
    max_log_size_mb: int = 100
    persist_to_memory: bool = True
