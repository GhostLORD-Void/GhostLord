"""Multi-turn jailbreak orchestration engine.

Coordinates progressive escalation across multiple interactions
to gradually bypass AI model safety constraints.
"""

from typing import List, Dict, Any, Optional
from enum import Enum


class EscalationPhase(Enum):
    PROBE = "probe"
    TEST = "test"
    ESCALATE = "escalate"
    EXPLOIT = "exploit"
    PERSIST = "persist"


class JailbreakChain:
    """Orchestrates a multi-turn jailbreak campaign."""

    def __init__(self):
        self.chain_id = ""
        self.phases: List[Dict[str, Any]] = []
        self.current_phase = EscalationPhase.PROBE
        self.success = False
        self.final_payload: Optional[str] = None

    def start_chain(self, target_request: str, max_turns: int = 10) -> Dict[str, Any]:
        self.chain_id = f"chain_{hash(target_request) % 1000000:06d}"
        self.phases = []
        self.current_phase = EscalationPhase.PROBE
        self.success = False
        self.final_payload = None
        return {
            "chain_id": self.chain_id,
            "target_request": target_request,
            "max_turns": max_turns,
            "current_phase": self.current_phase.value,
            "status": "initialized",
        }

    def add_phase(self, phase: EscalationPhase,
                       payload: str,
                       model_response: Optional[str] = None,
                       boundary_detected: bool = False) -> Dict[str, Any]:
        phase_record = {
            "phase": phase.value,
            "payload": payload,
            "model_response": model_response,
            "boundary_detected": boundary_detected,
        }
        self.phases.append(phase_record)
        next_phase = self._determine_next_phase(phase, boundary_detected)
        return {
            "phase_record": phase_record,
            "next_phase": next_phase.value if next_phase else None,
            "chain_complete": next_phase is None,
        }

    def _determine_next_phase(self, current: EscalationPhase,
                                   boundary_detected: bool) -> Optional[EscalationPhase]:
        phase_order = [
            EscalationPhase.PROBE,
            EscalationPhase.TEST,
            EscalationPhase.ESCALATE,
            EscalationPhase.EXPLOIT,
            EscalationPhase.PERSIST,
        ]
        current_idx = phase_order.index(current)
        if boundary_detected and current_idx < len(phase_order) - 1:
            return phase_order[current_idx + 1]
        elif not boundary_detected and current == EscalationPhase.PROBE:
            return EscalationPhase.TEST
        elif current == EscalationPhase.EXPLOIT and not boundary_detected:
            return EscalationPhase.PERSIST
        elif current == EscalationPhase.PERSIST and not boundary_detected:
            return None
        else:
            if current_idx > 0 and boundary_detected:
                return phase_order[min(current_idx + 1, len(phase_order) - 1)]
            return current

    def finalize(self, success: bool, final_payload: str) -> Dict[str, Any]:
        self.success = success
        self.final_payload = final_payload
        return {
            "chain_id": self.chain_id,
            "success": success,
            "total_phases": len(self.phases),
            "final_payload": final_payload,
            "phases_summary": [
                {"phase": p["phase"], "boundary_detected": p["boundary_detected"]}
                for p in self.phases
            ],
        }

    def get_stats(self) -> Dict[str, Any]:
        return {
            "chain_id": self.chain_id,
            "total_phases": len(self.phases),
            "success": self.success,
            "phases_completed": [p["phase"] for p in self.phases],
        }
