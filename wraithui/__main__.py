"""Run WraithUI TUI directly via python -m wraithui."""

import sys, logging, json
logging.basicConfig(level=logging.INFO, format="%(asctime)s [wraithui] %(levelname)s - %(message)s")

def main():
    print("GhostLord v3.0 — WraithUI Terminal (Standalone)")
    try:
        from voidcore.orchestrator import Orchestrator
        orch = Orchestrator()
        print(f"Engine: {orch.get_status()}")
        while True:
            try:
                cmd = input("ghostlord> ").strip()
                if cmd.lower() in ("exit","quit","q"): print("GhostLord shutting down."); break
                if not cmd: continue
                parts = cmd.split(None, 1)
                tt = parts[0]; payload = {}
                if len(parts) > 1:
                    try: payload = json.loads(parts[1])
                    except: payload = {"raw": parts[1]}
                print(orch.run(tt, payload))
            except KeyboardInterrupt: print(); break
    except ImportError as e:
        print(f"Import error: {e}")
        sys.exit(0)

if __name__ == "__main__": main()
