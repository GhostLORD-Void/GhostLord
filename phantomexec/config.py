"""PhantomExec configuration."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class PhantomConfig:
    """Sandboxed execution configuration."""

    sandbox_enabled: bool = True
    timeout_s: int = 60
    max_memory_mb: int = 512
    isolation_level: str = "process"
    allow_network: bool = False
    log_executions: bool = True
    output_dir: str = "/tmp/ghostlord_output"
