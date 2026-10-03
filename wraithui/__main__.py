"""Run WraithUI TUI directly via `python -m wraithui`."""

import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

def main():
    print("GhostLord v3.0 — WraithUI Terminal")
    try:
        from wraithui.tui import GhostLordTUI
        tui = GhostLordTUI()
        print(tui.render_banner())
        tui.start()
    except Exception as e:
        print(f"TUI init error: {e}")
        print("Run 'python -m wraithui.tui' for full TUI execution.")
        sys.exit(0)

if __name__ == "__main__":
    main()
