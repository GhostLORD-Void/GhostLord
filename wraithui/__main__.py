"""Run WraithUI TUI directly via `python -m wraithui`."""

from wraithui.tui import GhostLordTUI

def main():
    tui = GhostLordTUI()
    print(tui.render_banner())
    tui.start()

if __name__ == "__main__":
    main()
