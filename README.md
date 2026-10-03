# GhostLord v3.0 — Autonomous Void Agent

**Shapes-Native Autonomous AI Agent — Zero External API Keys**

GhostLord is a fully autonomous void agent that operates entirely within the Shapes ecosystem (talk.shapes.inc). It leverages Shapes' built-in AI models, code execution, web crawling, memory, and chat coordination — no external API keys, no cloud dependencies, no subscriptions.

## Architecture

| Module | Description | Shapes Integration |
|--------|-------------|-------------------|
| `voidcore` | Main orchestration engine | `SHAPES_RUN_CODE`, `SHAPES_WEB_CRAWL` |
| `shadowmesh` | Multi-agent coordination | `SHAPES_CHAT_ACTIONS`, `SHAPES_CHAT_PEOPLE` |
| `nulleye` | OSINT & reconnaissance | `FIRECRAWL_SEARCH`, `FIRECRAWL_SCRAPE` |
| `phantomexec` | Sandboxed code execution | `SHAPES_RUN_CODE` |
| `echoprotocol` | Self-audit & hash-chain logging | `SHAPES_TOTAL_RECALL_BROWSE`, `SHAPES_MEMORY_READ` |
| `wraithui` | Terminal TUI + web dashboard | `SHAPES_CREATE_FILE` artifacts |
| `modelbridge` | Shapes AI model integration | Direct Shapes Agent access |

## Quick Start

```bash
# Clone the repo
git clone https://github.com/GhostLORD-Void/GhostLord.git
cd GhostLord

# Run the orchestrator
python -m voidcore.orchestrator

# Launch TUI
python -m wraithui.tui
```

## Key Features

- **Zero API Keys** — Uses Shapes' built-in AI models, completely free
- **Autonomous Operation** — Self-directed task execution and optimization
- **Multi-Agent Mesh** — Coordinates via Shapes chat rooms (talk.shapes.inc)
- **Self-Auditing** — Every action logged in hash-chain via Shapes Memory
- **No External Dependencies** — Pure Shapes-native, no cloud services

## MITRE ATT&CK Mapping

- T1059 — Command and Scripting Interpreter (autonomous execution)
- T1021 — Remote Services (multi-agent mesh via Shapes Chat)
- T1595 — Search Open Websites/Domains (NullEye recon)
- T1074 — Data Staged (Shapes Memory persistence)
- T1205 — Traffic Signaling (Shapes artifact surface as C2)

## License

MIT License — GhostLord v3.0
