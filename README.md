# Tableau Dashboard Styler

## Overview

**Tableau Dashboard Styler** is a desktop tool for applying consistent, professional styling to Tableau dashboards. It automates the process of updating colors, fonts, layouts, and formatting across single or multiple dashboard files, ensuring brand consistency and visual appeal.

---

## Features (Planned)

* **Dashboard Parsing** - Read and analyze Tableau .twb and .twbx files
* **Style Application** - Apply custom color palettes, fonts, and layouts
* **Template Library** - Pre-built style templates for common use cases
* **Batch Processing** - Style multiple dashboards at once
* **Preview Mode** - See before/after comparisons
* **Safe Operations** - Automatic backup creation before modifications
* **Configuration Export/Import** - Share style configurations across projects

---

## Quick Start

### Prerequisites

* Windows 11
* Python 3.10+
* Git

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd Tableau_Styler

# Run setup script
.\scripts\setup.bat

# Run the application
.\scripts\run.bat
```

---

## Project Status

**Version:** 1.1.0  
**Status:** Initial Development  
**Current Milestone:** Project Setup & Core Foundation

---

## Technology Stack

* **Language:** Python 3.10+
* **XML Parsing:** lxml
* **UI Framework:** TBD (Tkinter/PyQt6/Web-based)
* **Configuration:** YAML/JSON
* **Build:** PyInstaller (Windows executable)
* **Testing:** pytest

---

## Project Structure

```
Tableau_Styler/
├── src/                 # Source code
│   ├── parser/          # Tableau file parsing
│   ├── styling/         # Styling engine
│   ├── ui/              # User interface
│   ├── config/          # Configuration management
│   └── utils/           # Helper utilities
├── tests/               # Unit and integration tests
├── assets/              # UI resources and sample files
├── scripts/             # Build and utility scripts
├── docs/                # Documentation
├── tickets/             # Feature and bug tracking
└── .claude/             # AI assistant memory and workflows
```

---

## Development Workflow

This project follows a structured AI-assisted development workflow:

* **Ticket-Driven**: Every feature and bug fix requires a ticket
* **Memory System**: Project context persists across AI sessions
* **Version Control**: All commits follow `[TICKET-####] Description` format
* **Documentation First**: Documentation updates alongside code changes

See [`.claude/CLAUDE.md`](.claude/CLAUDE.md) for complete workflow details.

---

## How It Works

### Tableau File Format

Tableau workbooks are XML-based:
* **.twb** - Uncompressed XML file
* **.twbx** - Compressed archive containing .twb and data sources

### Styling Process

1. **Parse** - Extract dashboard structure and current styling
2. **Transform** - Apply style rules to XML elements
3. **Validate** - Ensure changes don't break dashboard functionality
4. **Save** - Write modified workbook (with backup of original)

---

## Contributing

1. Review the project memory files in `.claude/memory/`
2. Create a ticket in `tickets/open/` before starting work
3. Follow coding conventions in `.claude/memory/coding_conventions.md`
4. Update documentation and changelog with changes
5. Commit with ticket reference: `[TICKET-####] Description`

---

## Roadmap

### Phase 1: Foundation (Current)
* Project setup and structure
* Basic Tableau file parsing
* Simple style application proof-of-concept

### Phase 2: Core Features
* Complete styling engine
* Template system
* Basic UI

### Phase 3: Advanced Features
* Batch processing
* Cloud integration (Tableau Server)
* AI-powered styling suggestions

---

## License

See [LICENSE](LICENSE) file for details.

---

## Documentation

* [Quick Start Guide](docs/QUICK_START.md)
* [Architecture](.claude/memory/architecture.md)
* [Project Memory](.claude/memory/project_memory.md)
* [Changelog](CHANGELOG.md)

---

## Version

Project Version: 1.1.0  
Framework Version: 1.1.0

---

**Built with the [AI Project Bootstrap Framework](https://github.com/Kvitekvist/claude_project_framework)**
