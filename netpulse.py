#!/usr/bin/env python3
"""NetPulse: basic DNS, TCP connectivity, and local interface diagnostics."""

import json
import shutil
import socket
import subprocess
import time
from datetime import datetime
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    console = Console()
except ImportError:
    console = None

TARGETS = [
    ("Cloudflare HTTPS", "1.1.1.1", 443),
    ("Google HTTPS", "8.8.8.8", 443),
]
DNS_HOSTS = ["example.com", "cloudflare.com"]


def show(message, style=None):
    if console:
        console.print(message, style=style)
    else:
        print(message)


def dns_results():
    rows = []
    show("\n--- DNS RESOLUTION ---", "bold cyan")
    for host in DNS_HOSTS:
        start = time.perf_counter()
        try:
            addresses = sorted({
                item[4][0] for item in socket.getaddrinfo(
                    host, 443, type=socket.SOCK_STREAM
                )
            })
            elapsed = round((time.perf_counter() - start) * 1000, 2)
            row = {"host": host, "status": "ok", "addresses": addresses,
                   "elapsed_ms": elapsed}
            show(f"{host:22} {', '.join(addresses)}  {elapsed:.2f} ms", "green")
        except OSError as exc:
            row = {"host": host, "status": "error", "error": str(exc)}
            show(f"{host:22} DNS FAILED: {exc}", "bold red")
        rows.append(row)
    return rows


def connectivity_results():
    rows = []
    show("\n--- TCP CONNECTIVITY ---", "bold cyan")
    for name, host, port in TARGETS:
        start = time.perf_counter()
        try:
            with socket.create_connection((host, port), timeout=3):
                elapsed = round((time.perf_counter() - start) * 1000, 2)
            row = {"name": name, "host": host, "port": port,
                   "status": "ok", "elapsed_ms": elapsed}
            show(f"{name:22} TCP OK  {elapsed:.2f} ms", "green")
        except OSError as exc:
            row = {"name": name, "host": host, "port": port,
                   "status": "error", "error": str(exc)}
            show(f"{name:22} FAILED: {exc}", "bold red")
        rows.append(row)
    return rows


def command_output(args):
    try:
        result = subprocess.run(
            args, capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() or result.stderr.strip() or "(no output)"
    except (OSError, subprocess.SubprocessError) as exc:
        return f"Unavailable: {exc}"


def interfaces():
    show("\n--- NETWORK INTERFACES ---", "bold cyan")
    ip = shutil.which("ip")
    result = command_output([ip, "-brief", "address"]) if ip else "Install iproute2 to use the ip command."
    show(result)
    return result


def default_route():
    show("\n--- DEFAULT ROUTE ---", "bold cyan")
    ip = shutil.which("ip")
    result = command_output([ip, "route", "show", "default"]) if ip else "Install iproute2 to use the ip command."
    show(result)
    return result


def save_report(report):
    path = Path("netpulse_report.json")
    try:
        path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        show(f"Report saved: {path.resolve()}", "bold green")
    except OSError as exc:
        show(f"Could not save report: {exc}", "bold red")


def main():
    last_report = {
        "timestamp": datetime.now().astimezone().isoformat(),
        "dns": [],
        "connectivity": [],
        "interfaces": None,
        "default_route": None,
    }
    while True:
        if console:
            console.print(Panel.fit(
                "[bold bright_cyan]NETPULSE[/bold bright_cyan]\n"
                "[white]Network diagnostics[/white]",
                border_style="bright_magenta"
            ))
        else:
            print("\n=== NETPULSE / NETWORK DIAGNOSTICS ===")

        print("1. Check DNS")
        print("2. Test public endpoint connectivity")
        print("3. Show local interfaces")
        print("4. Show default route")
        print("5. Run all checks")
        print("6. Save latest results to JSON")
        print("0. Exit")
        choice = input("Select > ").strip()

        if choice == "0":
            break
        elif choice == "1":
            last_report["dns"] = dns_results()
        elif choice == "2":
            last_report["connectivity"] = connectivity_results()
        elif choice == "3":
            last_report["interfaces"] = interfaces()
        elif choice == "4":
            last_report["default_route"] = default_route()
        elif choice == "5":
            last_report["dns"] = dns_results()
            last_report["connectivity"] = connectivity_results()
            last_report["interfaces"] = interfaces()
            last_report["default_route"] = default_route()
            last_report["timestamp"] = datetime.now().astimezone().isoformat()
        elif choice == "6":
            save_report(last_report)
        else:
            show("Invalid selection.", "yellow")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped safely.")
