"""Run VoidCore orchestrator directly via `python -m voidcore`."""

from voidcore.orchestrator import Orchestrator

def main():
    orch = Orchestrator()
    print(f"GhostLord v3.0 — VoidCore Orchestrator Started")
    print(f"Status: {orch.bridge.get_status()}")
    orch.run_autonomous_loop(iterations=1)

if __name__ == "__main__":
    main()
