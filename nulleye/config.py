"""NullEye configuration."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class NullEyeConfig:
    """OSINT reconnaissance configuration."""

    max_targets: int = 100
    default_tools: List[str] = field(default_factory=lambda: [
        "FIRECRAWL_SEARCH",
        "FIRECRAWL_SCRAPE",
    ])
    rate_limit_delay_s: float = 1.0
    user_agent: str = "GhostLord/3.0"
    follow_redirects: bool = True
    timeout_s: int = 30
