"""Run VoidCore orchestrator directly via `python -m voidcore`."""

import sys
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [voidcore] %(levelname)s - %(message)s",
)

def main():
    print("GhostLord v3.0 — VoidCore Standalone Termux Agent")
    print("=" * 50)
    print("Hinglish/NLP command parser ACTIVE")
    print("Type commands in Hinglish or English — real Termux execution")
    print("")

    from voidcore.orchestrator import Orchestrator
    orch = Orchestrator()

    status = orch.get_status()
    print(f"Engine: {status['engine']} v{status['version']}")
    print(f"Platform: {status['platform']}")
    print(f"Parser: {status['parser']}")
    print("")
    print("Examples:")
    print("  scan karo 192.168.1.1")
    print("  recon karo target.com")
    print("  run whoami")
    print("  crack karo hash.txt")
    print("  exploit target 192.168.1.1")
    print("  enum 192.168.1.1")
    print("  status")
    print("  exit")
    print("")

    while True:
        try:
            user_input = input("ghostlord> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "q"):
                print("GhostLord shutting down.")
                break

            # Use the Hinglish NLP parser
            result = orch.parse_and_run(user_input)
            print(json.dumps(result, indent=2))

        except KeyboardInterrupt:
            print()
            print("GhostLord shutting down.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
