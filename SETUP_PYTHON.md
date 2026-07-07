# Embedded Python Setup Instructions

This project uses a **portable, embedded Python** distribution that requires no system-wide installation.

## Status

✅ **Python 3.11.9 is already set up!**

The embedded Python is located in `.python/` directory with all dependencies installed.

## Dependencies Installed

- ✅ lxml (XML parsing)
- ✅ pyyaml (YAML configuration)
- ✅ pytest (testing)
- ✅ pytest-cov (code coverage)
- ✅ black (code formatting)
- ✅ pylint (linting)

## Usage

### Run Python Scripts

```bash
# Use the portable launcher
.\run_python.bat script_name.py

# Or call Python directly
.\.python\python.exe script_name.py
```

### Run Tests

```bash
.\run_python.bat test_manual.py
```

### Install Additional Packages

```bash
.\.python\python.exe -m pip install package_name
```

## Distribution

This setup is **fully portable** and can be distributed:

1. The entire project folder can be copied to any Windows machine
2. No Python installation required on target machine
3. All dependencies are self-contained in `.python/`

## Rebuilding from Scratch

If you need to rebuild the Python environment:

```bash
# Download Python embeddable package
curl -L -o python-embed.zip "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip"

# Extract to .python directory
unzip python-embed.zip -d .python

# Enable site packages (edit .python/python311._pth)
# Uncomment: import site
# Add line: Lib/site-packages

# Install pip
curl -L -o get-pip.py "https://bootstrap.pypa.io/get-pip.py"
.\.python\python.exe get-pip.py

# Install dependencies
.\.python\python.exe -m pip install -r requirements.txt
```

## Why Embedded Python?

✅ **No installation required** - Works immediately
✅ **Portable** - Entire project can be moved/shared
✅ **Isolated** - Doesn't interfere with system Python
✅ **Distributable** - Ship complete application
✅ **Consistent** - Everyone uses same Python version

## File Structure

```
Tableau_Styler/
├── .python/                 # Embedded Python 3.11.9
│   ├── python.exe           # Python interpreter
│   ├── Lib/                 # Standard library
│   │   └── site-packages/   # Installed packages (lxml, pyyaml, etc.)
│   └── Scripts/             # Pip, pytest, etc.
├── run_python.bat           # Convenient launcher
└── requirements.txt         # Package dependencies
```

## Notes

- The `.python/` directory is excluded from git (`.gitignore`)
- Size: ~50MB (Python) + ~20MB (dependencies) = ~70MB total
- Python 3.11.9 chosen for stability and compatibility
