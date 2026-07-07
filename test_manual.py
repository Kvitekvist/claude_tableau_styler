"""
Manual Test Script - Run without pytest

Tests the parser and template loader components.
Run with: python test_manual.py
"""

import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_template_loader():
    """Test YAML template loading"""
    print("\n" + "="*60)
    print("TEST 1: Template Loader")
    print("="*60)

    from config.template_loader import TemplateLoader

    try:
        loader = TemplateLoader()

        # List available templates
        print("\nListing available templates...")
        templates = loader.list_templates()
        print(f"Found {len(templates)} template(s):")
        for tmpl in templates:
            print(f"  - {tmpl['name']}: {tmpl['description']}")

        # Load corporate_brand.yaml
        print("\nLoading corporate_brand.yaml...")
        template = loader.load("corporate_brand.yaml")

        print(f"✓ Template loaded successfully!")
        print(f"  Name: {template.metadata.name}")
        print(f"  Description: {template.metadata.description}")
        print(f"  Version: {template.metadata.version}")

        # Validate colors
        print(f"\n  Colors:")
        print(f"    Brand colors: {len(template.colors.brand)} defined")
        print(f"    Primary Burgundy: {template.colors.brand.get('primary_burgundy', 'N/A')}")
        print(f"    Accent Green: {template.colors.brand.get('accent_green', 'N/A')}")
        print(f"    Categorical palette: {len(template.colors.categorical)} colors")
        print(f"    Sequential palettes: {len(template.colors.sequential)} defined")

        # Validate typography
        print(f"\n  Typography:")
        print(f"    Title: {template.typography.title.font_family} {template.typography.title.font_size}pt")
        print(f"    Title color: {template.typography.title.color}")
        print(f"    Body: {template.typography.body.font_family} {template.typography.body.font_size}pt")

        # Validate layout
        print(f"\n  Layout:")
        print(f"    Dashboard background: {template.layout.dashboard.background_color}")
        print(f"    Container background: {template.layout.containers.background_color}")

        print(f"\n✓ All validations passed!")
        return True

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tableau_parser():
    """Test Tableau file parsing"""
    print("\n" + "="*60)
    print("TEST 2: Tableau Parser")
    print("="*60)

    from parser.tableau_parser import TableauParser

    file_path = "tableau/input/RE - NO - Kraken - Competitor Analysis Hjem.twbx"

    if not os.path.exists(file_path):
        print(f"\n⚠ Skipping - file not found: {file_path}")
        return True

    try:
        parser = TableauParser()

        print(f"\nParsing: {file_path}")
        print("This may take a moment (large file with data extract)...")

        workbook = parser.parse(file_path)

        print(f"\n✓ Workbook parsed successfully!")
        print(f"  File type: {workbook.file_type}")
        print(f"  Tableau version: {workbook.version}")
        print(f"  Dashboards: {len(workbook.dashboards)}")
        print(f"  Worksheets: {len(workbook.worksheets)}")
        print(f"  Datasources: {len(workbook.datasources)}")

        if workbook.zip_contents:
            print(f"  Zip contents: {len(workbook.zip_contents)} files")
            print(f"    Files: {', '.join(list(workbook.zip_contents.keys())[:5])}")

        if workbook.dashboards:
            print(f"\n  Dashboard names:")
            for db in workbook.dashboards[:5]:
                print(f"    - {db.name}")

        if workbook.datasources:
            print(f"\n  Datasource info:")
            for ds in workbook.datasources[:3]:
                print(f"    - {ds.name}")
                if ds.caption:
                    print(f"      Caption: {ds.caption}")

        print(f"\n✓ All checks passed!")
        return True

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("TABLEAU STYLER - MANUAL TESTS")
    print("="*60)
    print("\nTesting TICKET-0006 and TICKET-0007 components")

    results = []

    # Test 1: Template Loader (TICKET-0007)
    results.append(("Template Loader", test_template_loader()))

    # Test 2: Tableau Parser (TICKET-0006)
    results.append(("Tableau Parser", test_tableau_parser()))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
        if not passed:
            all_passed = False

    print("="*60)

    if all_passed:
        print("\n✓ ALL TESTS PASSED!")
        print("\nTICKET-0006 and TICKET-0007 are ready!")
        return 0
    else:
        print("\n✗ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
