"""Run VoidCore orchestrator directly via python -m voidcore."""

import sys, logging, json
logging.basicConfig(level=logging.INFO, format="%(asctime)s [voidcore] %(levelname)s - %(message)s")

def main():
    print("GhostLord v3.0 — VoidCore Standalone Termux Agent")
    print("=" * 50)
    from voidcore.orchestrator import Orchestrator
    orch = Orchestrator()
    s = orch.get_status()
    print(f"Status: {s}")
    print("Available: recon | scan | execute | crawl | exploit | crack | exfil | enum")
    print("")
    while True:
        try:
            u = input("ghostlord> ").strip()
            if not u: continue
            if u.lower() in ("exit","quit","q"): print("GhostLord shutting down."); break
            parts = u.split(None, 1)
            tt = parts[0]; payload = {}
            if len(parts) > 1:
                try: payload = json.loads(parts[1])
                except: payload = {"raw": parts[1]}
            r = orch.run(tt, payload)
            print(json.dumps(r, indent=2))
        except KeyboardInterrupt: print(); break
        except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": main()
