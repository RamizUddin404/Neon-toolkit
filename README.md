<div align="center">

# ⚡ NEON TOOLKIT

### Android diagnostics · Safe file automation · Network monitoring

**A Termux-friendly Python toolkit for clear diagnostics, careful file handling, and practical connectivity checks.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Android](https://img.shields.io/badge/Platform-Android%20%7C%20Termux-3DDC84?style=for-the-badge&logo=android&logoColor=white)](https://termux.dev/)
[![Terminal UI](https://img.shields.io/badge/UI-Rich%20Terminal-00D9FF?style=for-the-badge)](https://github.com/Textualize/rich)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

</div>

---

## ✨ Overview

**Neon Toolkit** is a collection of Python command-line utilities for Android and Termux. It brings three everyday tasks into one consistent project:

- **DroidCheck** — inspect common Android build properties, storage, memory, battery information when readable, and root availability.
- **FilePilot** — list and search files, calculate folder sizes, report duplicate content by SHA-256, and make confirmation-based backup copies.
- **NetPulse** — check DNS resolution, test TCP connectivity to selected public endpoints, and inspect available network interface and route information.

The project is designed to be understandable, lightweight, and cautious by default. It uses rich colors and panels when the optional Rich package is installed, with a plain-text fallback where supported.

> **Status:** Educational utility toolkit. Some features depend on Android version, Termux permissions, installed packages, network access, and device manufacturer restrictions. It is not a device-unlocking tool or a full Android management suite.

## 🧭 Contents

- [Features](#-features)
- [Project structure](#-project-structure)
- [Requirements](#-requirements)
- [Install on Android / Termux](#-install-on-android--termux)
- [Run the toolkit](#-run-the-toolkit)
- [Tool reference](#-tool-reference)
- [File safety and privacy](#-file-safety-and-privacy)
- [Troubleshooting](#-troubleshooting)
- [Development and contributions](#-development-and-contributions)
- [About the maintainer](#-about-the-maintainer)
- [License](#-license)

## 🚀 Features

### 📱 DroidCheck — Android system diagnostics

- Reads common Android properties using getprop.
- Reports manufacturer, model, Android release, SDK level, and architecture where available.
- Displays storage information for the current user's home directory.
- Reads battery capacity, status, and temperature only if Android exposes those files to the process.
- Performs a best-effort check for available root access; it does not change root settings.
- Shows basic memory information when the system permits it.

### 🗂️ FilePilot — file automation

- Lists entries in a chosen folder.
- Searches for filenames by a text fragment.
- Finds files with matching SHA-256 content hashes.
- Calculates total folder size.
- Copies a folder to a destination after an explicit confirmation.
- Does **not** include automatic deletion or silent file cleanup.

**Backup note:** FilePilot is a convenience copy tool, not a verified backup system. Check the destination and open sample files after copying. Avoid using the source folder as its own destination or selecting a destination inside the source.

### 🌐 NetPulse — network monitoring

- Resolves selected public DNS names.
- Measures elapsed time for DNS lookups.
- Tests TCP connectivity to configured public endpoints on port 443.
- Displays network interfaces and the default route when the ip command is available.
- Can write a JSON report template for later reference.

Latency results depend on network conditions, routing, DNS caching, and Android background restrictions. A failed test does not automatically mean the internet connection is entirely down.

## 📁 Project structure

    Neon-toolkit/
    ├── README.md             # Project overview and documentation
    ├── neon_toolkit.py       # Unified interactive launcher
    ├── droidcheck.py         # Android system diagnostics
    ├── filepilot.py          # File search, reports, and backup copying
    ├── netpulse.py           # DNS and connectivity checks
    ├── requirements.txt      # Optional terminal UI dependency
    ├── .gitignore            # Generated files and local secrets exclusions
    ├── LICENSE               # MIT license
    ├── CONTRIBUTING.md       # Contribution guide
    └── SECURITY.md           # Security reporting and safe-use notes

## 🧰 Requirements

- Android with [Termux](https://termux.dev/) or another Python 3 environment.
- Python 3.10 or newer recommended.
- Internet access for NetPulse's public endpoint checks.
- Optional Termux package: iproute2, which provides the ip command for interface and route details.
- Optional Termux package: android-tools, which provides ADB tools for separate device debugging.
- Optional Python dependency: Rich for a colorful terminal interface.

No root access is required for the normal features. Root access does not guarantee that Android will expose protected information.

## 📲 Install on Android / Termux

Update Termux packages:

    pkg update && pkg upgrade
    pkg install python git

Clone the repository:

    git clone https://github.com/RamizUddin404/Neon-toolkit.git
    cd Neon-toolkit

Install the optional UI dependency and network utility:

    python -m pip install -r requirements.txt
    pkg install iproute2

For FilePilot access to shared storage, grant Android's storage permission when Termux requests it:

    termux-setup-storage

Only grant permissions you understand and need. On recent Android versions, storage access remains restricted by Android's scoped-storage rules.

## ▶️ Run the toolkit

Start the unified menu:

    python neon_toolkit.py

Or launch an individual tool:

    python droidcheck.py
    python filepilot.py
    python netpulse.py

## 🧪 Tool reference

| Tool | Main purpose | Writes files? | Network access? |
|---|---|---:|---:|
| DroidCheck | Read device/system diagnostics | No | No |
| FilePilot | Search, hash, size and backup copy | Only when a backup is requested | No |
| NetPulse | DNS and TCP connectivity checks | Only when a report is requested | Yes |

## 🔐 File safety and privacy

- Inspect paths before running file operations.
- FilePilot asks for the exact word BACKUP before copying.
- FilePilot does not delete source files.
- Do not use backup destinations that contain the source directory.
- Avoid running scripts from unknown sources with elevated privileges.
- Do not commit passwords, API keys, access tokens, private keys, personal documents, device identifiers, or private logs to GitHub.
- Network checks connect only to the public endpoints listed in the code; use only endpoints you are permitted to test.
- These scripts do not bypass Android screen locks, access other users' private files, or disable Android security controls.

## 🛠️ Troubleshooting

**Rich is missing**

    python -m pip install rich

**The ip command is unavailable**

    pkg install iproute2

**Storage path is inaccessible**

Run termux-setup-storage, approve the Android permission prompt, and check that the selected path exists. Some Android folders remain inaccessible to Termux by design.

**Battery values show “Unavailable”**

This is expected on devices where Android does not expose the relevant sysfs entries to ordinary apps or Termux.

**NetPulse cannot connect**

Check that mobile data or Wi-Fi is enabled. A network, firewall, VPN, DNS policy, or provider may block a test endpoint. The toolkit does not attempt to bypass those restrictions.

**Root status is “Not confirmed”**

A su executable being present does not prove root access. The root manager may deny the request, or the device may not be rooted.

## 🤝 Development and contributions

Bug reports, careful improvements, documentation updates, and platform compatibility fixes are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

For security-related concerns, see [SECURITY.md](SECURITY.md).

## 👤 About the maintainer

**GitHub:** [@RamizUddin404](https://github.com/RamizUddin404)

The maintainer's publicly shared technical interests include Python utilities, Android/Termux workflows, device diagnostics, networking, and practical automation. This section intentionally focuses on project-relevant information rather than publishing private personal details.

- GitHub profile: https://github.com/RamizUddin404
- Project repository: https://github.com/RamizUddin404/Neon-toolkit

## 📄 License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for the full text.

---

<div align="center">

**Built for learning. Designed for clarity. Careful with your data.**

</div>
