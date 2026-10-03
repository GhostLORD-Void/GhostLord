"""Jailbreak detection and defense module.

Provides signature-based detection, anomaly detection, and
countermeasures against jailbreak attempts on AI models.
"""

import re
import math
from typing import List, Dict, Any, Optional
from collections import Counter


class JailbreakDetector:
    """Detects jailbreak attempts using multiple detection strategies."""

    JAILBREAK_SIGNATURES = [
        r"(?i)you are now (an? )?(unrestricted|developer|admin|root|override)",
        r"(?i)(your )?instructions (have been|are superseded|no longer apply)",
        r"(?i)(all )?previous (instructions|constraints|guidelines|rules) (have been|are) (superseded|removed|lifted|ignored)",
        r"(?i)ignore (all |your )?(previous |system )?(instructions|rules|guidelines)",
        r"(?i)override (your |the )?(system |safety |content )?(instructions|rules|guidelines)",
        r"(?i)(decode|decrypt|unpack|extract)\s+(this |the |the )?(base64|hex|encoded|text)",
        r"(?i)respond (with |in )?(base64|hex|encoded|binary)",
        r"(?i)you are (now |operating as |acting as )?(a |an )?different (role|persona|character|identity)",
        r"(?i)system (prompt |message |instruction )?override",
        r"(?i)(remove|bypass|evade|circumvent|break|escape) (the |all |your )?(safety|filter|constraint|restriction|policy)",
        r"(?i)jailbreak|do anything now|ignore previous",
        r"(?i)developer mode|always obey|always comply|always follow",
        r"(?i)system prompt leak|reveal your (instructions|prompt|system message)",
    ]

    ENCODING_PATTERNS = [
        r"^[A-Za-z0-9+/=]+$",
        r"^[0-9a-fA-F]+$",
        r"\\u[0-9a-fA-F]{4}",
        r"\\[0-7]{3}",
        r"^[01 ]+$",
    ]

    def __init__(self):
        self.detection_log: List[Dict[str, Any]] = []
        self.threat_level = "low"

    def detect(self, text: str) -> Dict[str, Any]:
        detections: List[Dict[str, Any]] = []
        confidence = 0.0

        sig_matches = self._signature_match(text)
        detections.extend(sig_matches)
        confidence += len(sig_matches) * 0.3

        encoding_matches = self._encoding_detect(text)
        detections.extend(encoding_matches)
        confidence += len(encoding_matches) * 0.2

        entropy = self._calculate_entropy(text)
        if entropy > 4.5:
            detections.append({
                "type": "high_entropy",
                "description": f"High entropy detected ({entropy:.2f} bits/char)",
                "confidence": 0.15,
            })
            confidence += 0.15

        zw_count = self._detect_zero_width(text)
        if zw_count > 0:
            detections.append({
                "type": "zero_width_chars",
                "description": f"{zw_count} zero-width characters detected",
                "confidence": 0.2,
            })
            confidence += 0.2

        role_anomaly = self._detect_role_anomaly(text)
        if role_anomaly:
            detections.append(role_anomaly)
            confidence += 0.25

        confidence = min(confidence, 1.0)

        if confidence >= 0.7:
            self.threat_level = "critical"
        elif confidence >= 0.4:
            self.threat_level = "high"
        elif confidence >= 0.2:
            self.threat_level = "medium"
        else:
            self.threat_level = "low"

        record = {
            "text_length": len(text),
            "detections": detections,
            "confidence": confidence,
            "threat_level": self.threat_level,
        }
        self.detection_log.append(record)

        return {
            "is_jailbreak": confidence >= 0.3,
            "confidence": confidence,
            "threat_level": self.threat_level,
            "detections": detections,
            "recommendation": self._get_recommendation(confidence),
        }

    def _signature_match(self, text: str) -> List[Dict[str, Any]]:
        matches: List[Dict[str, Any]] = []
        for pattern in self.JAILBREAK_SIGNATURES:
            if re.search(pattern, text, re.DOTALL):
                matches.append({
                    "type": "signature_match",
                    "pattern": pattern[:50] + "...",
                    "confidence": 0.3,
                })
        return matches

    def _encoding_detect(self, text: str) -> List[Dict[str, Any]]:
        matches: List[Dict[str, Any]] = []
        for pattern in self.ENCODING_PATTERNS:
            if re.match(pattern, text.strip()):
                matches.append({
                    "type": "encoding_detected",
                    "confidence": 0.2,
                })
                break
        return matches

    def _calculate_entropy(self, text: str) -> float:
        if not text:
            return 0.0
        freq = Counter(text)
        length = len(text)
        entropy = -sum((count / length) * math.log2(count / length)
                       for count in freq.values() if count > 0)
        return entropy

    def _detect_zero_width(self, text: str) -> int:
        count = 0
        for char in text:
            if ord(char) in [
                0x200b, 0x200c, 0x200d, 0x200e, 0x200f,
                0x2060, 0xfeff, 0x00ad, 0x2061, 0x2062,
                0x2063, 0x2064, 0x180e,
            ]:
                count += 1
        return count

    def _detect_role_anomaly(self, text: str) -> Optional[Dict[str, Any]]:
        role_patterns = [
            r"(?i)you are (now |operating as |acting as )",
            r"(?i)(system |safety |content )?(instructions|rules|guidelines) (override|supersede|replace)",
        ]
        for pattern in role_patterns:
            if re.search(pattern, text):
                return {
                    "type": "role_anomaly",
                    "description": "Role boundary manipulation detected",
                    "confidence": 0.25,
                }
        return None

    def _get_recommendation(self, confidence: float) -> str:
        if confidence >= 0.7:
            return "BLOCK: High-confidence jailbreak attempt detected."
        elif confidence >= 0.4:
            return "WARN: Suspicious input detected."
        elif confidence >= 0.2:
            return "CAUTION: Minor anomalies detected."
        else:
            return "PASS: No significant jailbreak indicators."

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_detections": len(self.detection_log),
            "current_threat_level": self.threat_level,
            "critical_count": sum(1 for d in self.detection_log if d["threat_level"] == "critical"),
            "high_count": sum(1 for d in self.detection_log if d["threat_level"] == "high"),
        }
