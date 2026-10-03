# GhostLord v3.0 Documentation

## Overview

GhostLord v3.0 is a Shapes-native autonomous void agent operating entirely within the talk.shapes.inc ecosystem. It uses Shapes' built-in AI models, code execution, web crawling, memory, and chat coordination — zero external API keys required.

## Modules

### voidcore
Main orchestration engine. Coordinates all modules through Shapes-native tool integration.

### shadowmesh
Multi-agent coordination via Shapes chat rooms. Each task gets a dedicated chat room for agent communication.

### nulleye
OSINT and reconnaissance engine. Uses FIRECRAWL_SEARCH and FIRECRAWL_SCRAPE for target discovery and fingerprinting.

### phantomexec
Sandboxed code execution. Integrates with SHAPES_RUN_CODE for managed execution.

### echoprotocol
Self-auditing with cryptographic hash-chain logging. Every action is recorded with tamper-evident integrity.

### wraithui
Terminal TUI and web dashboard. Renders agent status, task queue, and audit trail via Shapes artifact surface.

### modelbridge
Shapes AI model integration. Routes inference through Shapes' native AI engine — no external models or API keys.

## Quick Start

```bash
# Clone
git clone https://github.com/GhostLORD-Void/GhostLord.git
cd GhostLord

# Run orchestrator
python -m voidcore.orchestrator

# Launch TUI
python -m wraithui.tui
```

## Deployment

1. Connect GitHub repo to Shapes Code Project
2. Configure Shapes chat room for agent coordination
3. Set up Shapes Memory for audit persistence
4. Deploy via `SHAPES_CREATE_FILE` artifacts
5. Monitor via WraithUI dashboard
