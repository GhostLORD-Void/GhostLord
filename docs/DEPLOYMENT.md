# GhostLord v3.0 Deployment Guide

## Prerequisites

- Shapes account (talk.shapes.inc)
- GitHub account (for repo hosting)
- No API keys required

## Deployment Steps

### 1. Clone Repository

```bash
git clone https://github.com/GhostLORD-Void/GhostLord.git
cd GhostLord
```

### 2. Connect to Shapes

- Go to Shapes Code Projects settings
- Connect the GhostLord GitHub repo
- Shapes will auto-detect the project structure

### 3. Configure Chat Room

- Create a Shapes chat room for GhostLord coordination
- Note the room ID for shadowmesh configuration
- Set up multi-agent communication channels

### 4. Initialize Memory

- Configure Shapes Memory for audit persistence
- EchoProtocol will automatically log all actions
- Hash-chain integrity verified on each session

### 5. Deploy

```bash
# Run the orchestrator
python -m voidcore.orchestrator

# Launch the TUI
python -m wraithui.tui

# Or start the dashboard
python -m wraithui.dashboard
```

## Monitoring

- WraithUI dashboard at `http://localhost:8080`
- Audit logs via Shapes Memory
- Task metrics via echoprotocol

## Updating

```bash
git pull origin main
# No dependency changes needed — fully Shapes-native
```
