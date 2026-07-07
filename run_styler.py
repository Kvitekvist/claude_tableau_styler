"""
Tableau Dashboard Styler - Runner Script

Handles proper path setup and runs the main application.
"""

import sys
import os

# Add src directory to Python path
src_dir = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_dir)

# Import and run main
from main import main

if __name__ == "__main__":
    sys.exit(main())
