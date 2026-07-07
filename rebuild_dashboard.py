"""
Rebuild Dashboard Script

Creates a professionally designed dashboard following modern BI design guidelines.
"""

import sys
import os

# UTF-8 console support for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from parser.tableau_parser import TableauParser
from config.template_loader import TemplateLoader
from styling.engine import StylingEngine
from dashboard.dashboard_rebuilder import DashboardRebuilder
from utils.file_manager import FileManager


def main():
    print("=" * 60)
    print("TABLEAU DASHBOARD REBUILDER")
    print("=" * 60)
    print()

    input_file = "tableau/input/RE - NO - Kraken - Competitor Analysis Hjem.twbx"
    output_dir = "tableau/output"
    backup_dir = "tableau/backups"

    print("→ Parsing original workbook...")
    parser = TableauParser()
    workbook = parser.parse(input_file)
    print(f"  ✓ Parsed {workbook.file_type.upper()}")
    print(f"    Dashboards: {len(workbook.dashboards)}")
    print(f"    Worksheets: {len(workbook.worksheets)}")
    print()

    print("→ Rebuilding Hjem.no dashboard with modern layout...")
    rebuilder = DashboardRebuilder()
    rebuilt_workbook = rebuilder.rebuild_hjem_dashboard(workbook)
    print("  ✓ Dashboard restructured")
    print("    Layout: 12-column grid")
    print("    Structure: Tiled containers")
    print("    Spacing: 24px outer, 16-24px between sections")
    print()

    print("→ Loading corporate brand template...")
    loader = TemplateLoader()
    template = loader.load("corporate_brand.yaml")
    print(f"  ✓ Template loaded: {template.metadata.name}")
    print()

    print("→ Applying professional styling...")
    engine = StylingEngine()
    styled_workbook = engine.apply_template(rebuilt_workbook, template)
    print("  ✓ Styling applied")
    print("    Colors: Corporate burgundy & green")
    print("    Typography: Arial, standardized sizes")
    print("    Charts: Optimized for readability")
    print()

    print("→ Creating backup...")
    file_manager = FileManager()
    backup_path = file_manager.create_backup(input_file, backup_dir)
    print(f"  ✓ Backup: {os.path.basename(backup_path)}")
    print()

    print("→ Writing redesigned dashboard...")
    output_path = file_manager.write(styled_workbook, input_file, output_dir)
    print(f"  ✓ Output: {os.path.basename(output_path)}")
    print()

    print("=" * 60)
    print("✓ DASHBOARD REBUILD COMPLETE")
    print("=" * 60)
    print()
    print("New dashboard features:")
    print("  • Professional 12-column grid layout")
    print("  • Equal-width KPI cards with proper spacing")
    print("  • Visual hierarchy (trend chart largest)")
    print("  • Tiled container structure")
    print("  • Consistent 24px outer padding")
    print("  • 16-24px section spacing")
    print("  • Corporate colors & typography")
    print("  • Optimized table & chart formatting")
    print()
    print(f"Open in Tableau Desktop:")
    print(f"  {output_path}")
    print()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
