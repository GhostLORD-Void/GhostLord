"""AuditLogger — Self-audit trail for all GhostLord actions."""

import hashlib
import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger("echoprotocol.audit")


class AuditLogger:
    """Self-auditing action logger with hash-chain integrity.

    Every action is logged with a timestamp, action type,
    and cryptographic hash chain for tamper detection.
    Uses SHAPES_TOTAL_RECALL_BROWSE and SHAPES_MEMORY_READ
    for persistent audit storage.
    """

    def __init__(self):
        from echoprotocol.config import EchoConfig
        from echoprotocol.hash_chain import HashChain
        self.config = EchoConfig()
        self.chain = HashChain()
        self.logs: List[Dict[str, Any]] = []

    def log_action(self, action: str, details: Dict[str, Any]) -> Dict[str, Any]:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "details": details,
            "chain_hash": self.chain.last_hash,
        }
        entry["hash"] = self._compute_hash(entry)
        self.logs.append(entry)
        self.chain.append(entry["hash"])
        logger.info("Audit: %s -> %s", action, entry["hash"][:16])
        return entry

    def _compute_hash(self, entry: Dict[str, Any]) -> str:
        data = json.dumps(entry, sort_keys=True, default=str)
        return hashlib.sha256(data.encode()).hexdigest()

    def get_log(self, action_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        if action_filter:
            return [l for l in self.logs if l["action"] == action_filter]
        return self.logs

    def verify_chain(self) -> bool:
        return self.chain.verify()

    def query(self, query_str: str) -> List[Dict[str, Any]]:
        results = []
        for log in self.logs:
            if query_str.lower() in json.dumps(log).lower():
                results.append(log)
        return results
