#!/usr/bin/env python3
"""DroidCheck: read-only Android and Termux diagnostics."""

import os
import platform
import shutil
import subprocess
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    console = Console()
except ImportError:
    console = None


def command(args, timeout=4):
    try:
        result = subprocess.run(
            args, capture_output=True, text=True, timeout=timeout
        )
        return (result.stdout or result.stderr).strip()
    except (OSError, subprocess.SubprocessError) as exc:
        return f"Unavailable: {exc}"


def prop(key):
    value = command(["getprop", key])
    return value if value and not value.startswith("Unavailable:") else "Unknown"


def root_status():
    su = shutil.which("su")
    if not su:
        return "Not detected"
    result = command([su, "-c", "id"], timeout=3)
    if "uid=0" in result:
        return "Root available"
    if "permission denied" in result.lower():
        return "Denied by root manager"
    return "Not confirmed"


def storage_info():
    try:
        usage = shutil.disk_usage(Path.home())
        return (
            f"{usage.total / 2**30:.2f} GiB total, "
            f"{usage.used / 2**30:.2f} GiB used, "
            f"{usage.free / 2**30:.2f} GiB free"
        )
    except OSError as exc:
        return f"Unavailable: {exc}"


def battery_info():
    base = Path("/sys/class/power_supply/battery")
    values = {}
    for name in ("capacity", "status", "temperature"):
        try:
            raw = (base / name).read_text(encoding="utf-8").strip()
            if name == "capacity":
                raw += "%"
            elif name == "temperature":
                raw = f"{int(raw) / 10:.1f} °C"
            values[name.capitalize()] = raw
        except (OSError, ValueError):
            values[name.capitalize()] = "Unavailable"
    return values


def diagnostics():
    rows = [
        ("Manufacturer", prop("ro.product.manufacturer")),
        ("Model", prop("ro.product.model")),
        ("Android release", prop("ro.build.version.release")),
        ("SDK level", prop("ro.build.version.sdk")),
        ("Build type", prop("ro.build.type")),
        ("Architecture", platform.machine()),
        ("Python", platform.python_version()),
        ("Root status", root_status()),
        ("Home storage", storage_info()),
    ]
    rows.extend(battery_info().items())

    if console:
        table = Table(title="DROIDCHECK / SYSTEM STATUS", border_style="cyan")
        table.add_column("Property", style="bold cyan")
        table.add_column("Value", style="white")
        for key, value in rows:
            table.add_row(str(key), str(value))
        console.print(Panel(table, border_style="bright_blue"))
    else:
        print("\n=== DROIDCHECK / SYSTEM STATUS ===")
        for key, value in rows:
            print(f"{key:18}: {value}")

    try:
        memory = Path("/proc/meminfo").read_text(encoding="utf-8").splitlines()[:5]
        print("\n--- MEMORY (kernel-reported) ---")
        print("\n".join(memory))
    except OSError:
        print("\nMemory details unavailable.")

    print("\nRead-only checks complete. No system settings were changed.")


if __name__ == "__main__":
    diagnostics()
