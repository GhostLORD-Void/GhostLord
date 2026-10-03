"""Run VoidCore orchestrator directly via `python -m voidcore`."""

import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

def main():
    print("GhostLord v3.0 — VoidCore Orchestrator")
    print("Initializing...")
    try:
        from voidcore.orchestrator import Orchestrator
        orch = Orchestrator()
        print(f"Status: {orch.bridge.get_status()}")
        orch.run_autonomous_loop(iterations=1)
        print("Orchestrator run complete.")
    except Exception as e:
        print(f"Init error (expected in standalone mode): {e}")
        print("Run 'python -m voidcore.orchestrator' for full execution.")
        sys.exit(0)

if __name__ == "__main__":
    main()
