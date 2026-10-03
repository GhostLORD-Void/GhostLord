"""HashChain — Blockchain-style action integrity chain."""

import hashlib
from typing import List


class HashChain:
    """Cryptographic hash chain for audit log integrity.

    Each new entry is hashed with the previous entry's hash,
    creating an immutable chain. Tampering with any entry
    breaks the entire chain.
    """

    def __init__(self):
        self.chain: List[str] = []
        self._genesis()

    def _genesis(self) -> None:
        genesis_hash = hashlib.sha256(b"ghostlord_v3_genesis").hexdigest()
        self.chain.append(genesis_hash)

    def append(self, data: str) -> None:
        prev = self.chain[-1]
        new_hash = hashlib.sha256(f"{prev}:{data}".encode()).hexdigest()
        self.chain.append(new_hash)

    @property
    def last_hash(self) -> str:
        return self.chain[-1] if self.chain else ""

    def verify(self) -> bool:
        for i in range(1, len(self.chain)):
            expected = hashlib.sha256(
                f"{self.chain[i-1]}:{self.chain[i]}".encode()
            ).hexdigest()
            if self.chain[i] != expected:
                return False
        return True

    def length(self) -> int:
        return len(self.chain)
