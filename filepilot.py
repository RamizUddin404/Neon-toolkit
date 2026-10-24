#!/usr/bin/env python3
"""FilePilot: file listing, search, duplicate reporting, and backup copying."""

import hashlib
import os
import shutil
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    console = Console()
except ImportError:
    console = None
    Prompt = None


def say(message, style=None):
    if console:
        console.print(message, style=style)
    else:
        print(message)


def ask(message):
    if Prompt:
        return Prompt.ask(message)
    return input(f"{message}: ")


def valid_folder(raw):
    path = Path(raw).expanduser()
    if not path.exists() or not path.is_dir():
        say("Folder does not exist or is not a directory.", "bold red")
        return None
    return path.resolve()


def list_folder(root):
    try:
        entries = sorted(root.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        if not entries:
            say("Folder is empty.")
            return
        for path in entries:
            try:
                kind = "DIR " if path.is_dir() else "FILE"
                size = path.stat().st_size if path.is_file() else 0
                say(f"{kind:4}  {size:>12,} B  {path.name}")
            except OSError as exc:
                say(f"SKIP  {path.name}: {exc}", "yellow")
    except OSError as exc:
        say(f"Cannot read folder: {exc}", "bold red")


def search_names(root, term):
    matches = 0
    try:
        for current, dirs, files in os.walk(root, followlinks=False):
            dirs[:] = [d for d in dirs if not (Path(current) / d).is_symlink()]
            for name in dirs + files:
                path = Path(current) / name
                if term.casefold() in name.casefold():
                    say(str(path))
                    matches += 1
    except OSError as exc:
        say(f"Search error: {exc}", "bold red")
    say(f"\nMatches: {matches}")


def folder_size(root):
    total = 0
    for current, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if not (Path(current) / d).is_symlink()]
        for name in files:
            path = Path(current) / name
            try:
                if not path.is_symlink():
                    total += path.stat().st_size
            except OSError:
                pass
    return total


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def duplicate_report(root):
    seen = {}
    for current, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if not (Path(current) / d).is_symlink()]
        for name in files:
            path = Path(current) / name
            try:
                if path.is_symlink():
                    continue
                key = (path.stat().st_size, digest(path))
                seen.setdefault(key, []).append(path)
            except OSError as exc:
                say(f"Skipped {path}: {exc}", "yellow")

    groups = [paths for paths in seen.values() if len(paths) > 1]
    if not groups:
        say("No duplicate contents found.", "green")
        return
    for index, paths in enumerate(groups, 1):
        say(f"\nDuplicate group {index}:", "bold yellow")
        for path in paths:
            say(f"  {path}")
    say("\nReport only: no files were deleted.", "green")


def backup_folder(source, destination):
    src = source.resolve()
    dst = Path(destination).expanduser().resolve()

    if not src.is_dir():
        say("Source folder is unavailable.", "bold red")
        return
    # Reject source itself, destinations inside source, and its ancestors.
    # The ancestor check prevents copying a directory onto itself.
    if dst == src or src in dst.parents or dst in src.parents:
        say("Unsafe destination: choose a separate folder outside the source tree.", "bold red")
        return
    if dst.exists() and not dst.is_dir():
        say("Destination exists and is not a directory.", "bold red")
        return

    say(f"Source:      {src}")
    say(f"Destination: {dst}")
    say("This copies files and may replace same-named destination files.", "yellow")
    if ask("Type BACKUP to continue") != "BACKUP":
        say("Cancelled. No copy started.", "yellow")
        return

    try:
        dst.mkdir(parents=True, exist_ok=True)
        target = dst / src.name
        shutil.copytree(
            src, target, dirs_exist_ok=True, symlinks=False,
            ignore=shutil.ignore_patterns("__pycache__", ".DS_Store")
        )
        say(f"Backup copy completed: {target}", "bold green")
        say("Verify important files at the destination.", "yellow")
    except (OSError, shutil.Error) as exc:
        say(f"Backup failed or was partial: {exc}", "bold red")


def main():
    while True:
        if console:
            console.print(Panel.fit(
                "[bold bright_cyan]FILEPILOT[/bold bright_cyan]\n"
                "[white]Safe file automation[/white]",
                border_style="bright_blue"
            ))
        else:
            print("\n=== FILEPILOT / SAFE FILE AUTOMATION ===")

        print("1. List folder contents")
        print("2. Search filenames")
        print("3. Report duplicate content")
        print("4. Copy folder to backup")
        print("5. Calculate folder size")
        print("0. Exit")
        choice = input("Select > ").strip()

        if choice == "0":
            break
        if choice not in {"1", "2", "3", "4", "5"}:
            say("Invalid selection.", "yellow")
            continue

        raw = ask("Folder path")
        root = valid_folder(raw)
        if root is None:
            continue

        if choice == "1":
            list_folder(root)
        elif choice == "2":
            term = ask("Filename contains")
            if term:
                search_names(root, term)
        elif choice == "3":
            duplicate_report(root)
        elif choice == "4":
            backup_folder(root, ask("Backup destination"))
        elif choice == "5":
            say(f"Total size: {folder_size(root) / 2**20:.2f} MiB", "bold cyan")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled safely.")
