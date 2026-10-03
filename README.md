# GhostLord v3.0 — Autonomous Void Agent

Shapes-Native | Zero API Keys | Fully Standalone Termux Agent

## Quick Start

```bash
cd ~/GhostLord
git pull origin main
python -m voidcore
```

## Task Types

| Type | Payload | Description |
| :--- | :--- | :--- |
| recon | target, scan_type | nmap vuln scan |
| scan | target, ports | custom port scan |
| execute | code | run shell command |
| crawl | url, depth | HTTP crawl |
| exploit | target, port | Metasploit |
| crack | hash_file, hash_type | hashcat |
| exfil | data, exfil_url | data exfiltration |
| enum | target, port | SMB enum |

## Interactive Mode

```
ghostlord> recon {"target":"example.com","scan_type":"quick"}
ghostlord> execute {"code":"whoami"}
ghostlord> exit
```
