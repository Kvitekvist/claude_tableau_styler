# Technology Stack

This document is the authoritative reference for the project's technical environment.

Update it whenever the technology stack changes.

---

# Project Information

**Project Name:** Tableau Dashboard Styler

**Version:** 1.1.0

**Created:** 2026-07-07

---

# Programming Language

Language: Python

Version: 3.10+ (to be confirmed based on environment)

---

# Framework

Name: TBD (To be decided - options: Tkinter, PyQt6, or Flask/FastAPI)

Version: TBD

Purpose: User interface for dashboard styling configuration and preview

---

# Runtime

Python 3.10+

---

# Package Manager

pip (Python package manager)

Version: Latest with Python installation

---

# Build System

PyInstaller (for creating Windows executable)

Purpose: Package Python application into standalone .exe for distribution

---

# Development Environment

Operating System: Windows 11 Enterprise

IDE: VS Code

Compiler: N/A (Python is interpreted)

SDK: Python 3.10+

---

# Dependencies

List major dependencies.

| Library | Version | Purpose |
| ------- | ------- | ------- |
| lxml | Latest | XML parsing for Tableau .twb files |
| pyyaml | Latest | Configuration file management |
| PyQt6 OR tkinter | Latest | User interface (to be decided) |
| pytest | Latest | Unit testing |
| black | Latest | Code formatting |
| pylint | Latest | Code linting |

---

# External Services

* GitHub - Source code repository
* (Future: Tableau Server API for cloud integration)

---

# Storage

* Local file system - Tableau workbook files (.twb/.twbx)
* JSON/YAML - Style configuration files
* Local file system - User preferences and templates

---

# APIs

**Tableau File Format**
* Format: XML-based workbook files
* Documentation: Tableau Developer Documentation
* No API authentication required for local files
* (Future: Tableau Server REST API for cloud integration)

---

# Build Output

* Windows executable (.exe) - PyInstaller-built standalone application
* Installation package - Windows installer (future)

---

# Deployment

* GitHub Releases - Versioned releases with executable downloads
* Manual - Direct .exe distribution for now
* (Future: Windows Installer with auto-update capability)

---

# Required Tools

* Git - Version control
* Python 3.10+ - Runtime and development
* VS Code - Primary IDE
* pip - Package management

---

# Environment Variables

| Variable | Required | Description |
| -------- | -------- | ----------- |
| None currently | N/A | No environment variables required yet |

Do **not** store secrets in this file.

---

# Notes

Record important information about the project's technical ecosystem that will help future development sessions.
