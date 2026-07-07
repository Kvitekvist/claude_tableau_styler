# Project Architecture

## Overview

**Tableau Dashboard Styler** is designed as a desktop application that reads Tableau workbook files (.twb/.twbx), applies styling rules, and generates updated workbooks. The architecture follows a modular design separating file parsing, styling logic, and user interface.

---

## Components

### User Interface

**Technology**: TBD (Options: Tkinter, PyQt6, or web-based with Flask/FastAPI)

The UI provides:
- Dashboard preview/selection
- Style configuration interface
- Before/after comparison
- Batch processing controls
- Template management

### Tableau Parser

**Core Component**: Tableau workbook file parser

Responsibilities:
- Parse .twb (XML) and .twbx (zipped XML) files
- Extract dashboard structure, worksheets, formatting
- Build internal representation of dashboard elements
- Validate Tableau file format compatibility

### Styling Engine

**Core Logic**: Style application and transformation

Responsibilities:
- Apply color palettes to charts and visualizations
- Modify fonts, sizes, and spacing
- Update dashboard layout properties
- Apply formatting rules to worksheets
- Preserve data connections and calculations

### File Manager

**I/O Operations**: File reading, writing, backup

Responsibilities:
- Safe file reading/writing with backup creation
- Handle .twb (uncompressed) and .twbx (compressed) formats
- Version control for modified files
- Export styling configurations

### Configuration System

**Storage**: JSON/YAML-based style definitions

Responsibilities:
- Store style templates
- User preferences
- Custom color palettes
- Font configurations
- Layout rules

---

## Folder Responsibilities

- **`src/`** - Source code for all components
  - `src/parser/` - Tableau file parsing logic
  - `src/styling/` - Styling engine and rules
  - `src/ui/` - User interface components
  - `src/utils/` - Helper functions and utilities
  - `src/config/` - Configuration management
- **`tests/`** - Unit and integration tests
- **`assets/`** - UI resources, icons, sample files
- **`scripts/`** - Build, setup, and utility scripts
- **`docs/`** - User documentation and guides
- **`tickets/`** - Feature and bug tracking
- **`.claude/`** - AI assistant memory and workflows

---

## Dependencies

### Core Dependencies (To Be Determined)

**XML Parsing**:
- `lxml` or `xml.etree.ElementTree` - Parse Tableau .twb XML files

**File Handling**:
- `zipfile` - Handle .twbx compressed files
- `shutil` - File operations and backups

**Configuration**:
- `pyyaml` or `json` - Style configuration files

**UI Framework** (Choose one):
- `tkinter` (built-in, lightweight)
- `PyQt6` (professional, feature-rich)
- `Flask/FastAPI` + web frontend (browser-based)

---

## Design Principles

1. **Non-Destructive**: Always create backups before modifying files
2. **Modular**: Separate concerns (parsing, styling, UI) for testability
3. **Extensible**: Easy to add new styling rules and templates
4. **Safe**: Validate all file operations and XML modifications
5. **User-Friendly**: Clear error messages and intuitive workflows
6. **Reversible**: Support undo/restore operations

---

## Future Improvements

- **Plugin System**: Allow custom styling rules via plugins
- **Cloud Integration**: Connect to Tableau Server/Online API
- **AI Styling**: Machine learning-based styling suggestions
- **Collaboration**: Share and rate style templates
- **Performance**: Optimize for large workbooks with many dashboards
- **Cross-Platform**: Ensure compatibility on Windows, Mac, Linux
