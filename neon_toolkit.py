#!/usr/bin/env python3
"""Neon Toolkit launcher with a small animated terminal intro."""

import shutil
import subprocess
import sys
import time
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    console = Console()
except ImportError:
    console = None

ROOT = Path(__file__).resolve().parent
TOOLS = {
    "1": ("DroidCheck", "droidcheck.py"),
    "2": ("FilePilot", "filepilot.py"),
    "3": ("NetPulse", "netpulse.py"),
}


def intro():
    title = "NEON TOOLKIT"
    if console:
        console.clear()
        for i in range(1, len(title) + 1):
            console.print(
                Text(title[:i], style="bold bright_cyan"),
                end="\r"
            )
            time.sleep(0.025)
        console.print()
        console.print(Panel(
            "[bold white]Android utilities for Termux[/bold white]\n"
            "[cyan]Diagnostics[/cyan]  •  [green]File automation[/green]  •  "
            "[magenta]Network monitoring[/magenta]\n\n"
            "[dim]Safe defaults · Local-first · Permission-aware[/dim]",
            border_style="bright_blue",
            title="[bold bright_magenta]v1.0[/bold bright_magenta]"
        ))
    else:
        print("\n" + "=" * 42)
        print("NEON TOOLKIT")
        print("Android utilities for Termux")
        print("=" * 42)


def main():
    while True:
        intro()
        print("\n[1] DroidCheck  - Android diagnostics")
        print("[2] FilePilot   - File automation")
        print("[3] NetPulse    - Network monitoring")
        print("[4] Install/check optional dependencies")
        print("[0] Exit")
        choice = input("\nSelect > ").strip()

        if choice == "0":
            print("Goodbye. No background tasks were started.")
            return
        if choice in TOOLS:
            name, filename = TOOLS[choice]
            path = ROOT / filename
            if not path.is_file():
                print(f"Missing script: {path}")
                input("Press Enter to continue...")
                continue
            print(f"\nLaunching {name}...\n")
            try:
                subprocess.run([sys.executable, str(path)], check=False)
            except OSError as exc:
                print(f"Could not start {name}: {exc}")
            input("\nPress Enter to return to the main menu...")
        elif choice == "4":
            print("Python:", sys.version.split()[0])
            print("Rich UI:", "installed" if console else "not installed (plain text mode)")
            print("Git:", shutil.which("git") or "not found")
            print("ip:", shutil.which("ip") or "not found; install iproute2 in Termux")
            input("\nPress Enter to continue...")
        else:
            print("Invalid option.")
            time.sleep(0.8)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExited safely.")
