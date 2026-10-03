"""WraithUI configuration."""

from dataclasses import dataclass


@dataclass
class UIConfig:
    """Terminal and dashboard UI configuration."""

    theme: str = "dark"
    show_banner: bool = True
    refresh_interval_s: int = 5
    dashboard_port: int = 8080
    dashboard_host: str = "0.0.0.0"
    colors: dict = None

    def __post_init__(self):
        if self.colors is None:
            self.colors = {
                "primary": "#00ff88",
                "secondary": "#ff0040",
                "background": "#0a0a0a",
                "text": "#e0e0e0",
                "accent": "#4488ff",
            }
