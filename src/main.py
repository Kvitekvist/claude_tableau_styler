"""
Tableau Dashboard Styler - Main Application

Entry point for styling Tableau dashboards with template configurations.
"""

import sys
import os
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add src to path if running as script
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(__file__))

from parser.tableau_parser import TableauParser, InvalidTableauFileError
from config.template_loader import TemplateLoader, InvalidTemplateError
from styling.engine import StylingEngine, StylingEngineError
from utils.file_manager import FileManager, BackupFailedError, WriteFailedError


class TableauStylerApp:
    """Main application orchestrator"""

    def __init__(self):
        self.parser = TableauParser()
        self.loader = TemplateLoader()
        self.engine = StylingEngine()
        self.file_manager = FileManager()

    def style_dashboard(
        self,
        input_file: str,
        template_file: str = "corporate_brand.yaml"
    ) -> str:
        """
        Apply styling template to a Tableau dashboard

        Args:
            input_file: Path to .twb or .twbx file
            template_file: Path to style template YAML

        Returns:
            Path to styled output file

        Raises:
            Various exceptions on errors
        """
        print(f"\n{'='*60}")
        print(f"Styling: {Path(input_file).name}")
        print(f"{'='*60}\n")

        # Step 1: Parse workbook
        print("→ Parsing Tableau workbook...")
        try:
            workbook = self.parser.parse(input_file)
            print(f"  ✓ Parsed successfully")
            print(f"    Type: {workbook.file_type}")
            print(f"    Version: {workbook.version}")
            print(f"    Dashboards: {len(workbook.dashboards)}")
            print(f"    Worksheets: {len(workbook.worksheets)}")
        except InvalidTableauFileError as e:
            print(f"  ✗ ERROR: {e}")
            raise

        # Step 2: Load template
        print(f"\n→ Loading template: {template_file}...")
        try:
            template = self.loader.load(template_file)
            print(f"  ✓ Loaded successfully")
            print(f"    Template: {template.metadata.name}")
            print(f"    Version: {template.metadata.version}")
        except (FileNotFoundError, InvalidTemplateError) as e:
            print(f"  ✗ ERROR: {e}")
            raise

        # Step 3: Create backup
        print(f"\n→ Creating backup...")
        try:
            backup_path = self.file_manager.create_backup(input_file)
            print(f"  ✓ Backup created: {Path(backup_path).name}")
        except BackupFailedError as e:
            print(f"  ✗ ERROR: {e}")
            print(f"  ⚠ Aborting - cannot proceed without backup")
            raise

        # Step 4: Apply styling
        print(f"\n→ Applying styling transformations...")
        try:
            styled_workbook = self.engine.apply_template(workbook, template)
            print(f"  ✓ Styling applied successfully")
            print(f"    Colors: {len(template.colors.categorical)} categorical")
            print(f"    Typography: {template.typography.title.font_family} {template.typography.title.font_size}pt")
            print(f"    Layout: {template.layout.dashboard.background_color}")
        except StylingEngineError as e:
            print(f"  ✗ ERROR: {e}")
            raise

        # Step 5: Write output
        print(f"\n→ Writing styled output...")
        try:
            output_path = self.file_manager.write(styled_workbook, input_file)
            print(f"  ✓ Output written: {Path(output_path).name}")
        except WriteFailedError as e:
            print(f"  ✗ ERROR: {e}")
            raise

        # Success summary
        print(f"\n{'='*60}")
        print(f"✓ STYLING COMPLETE")
        print(f"{'='*60}")
        print(f"  Input:  {Path(input_file).name}")
        print(f"  Output: {Path(output_path).name}")
        print(f"  Backup: {Path(backup_path).name}")
        print(f"{'='*60}\n")

        return output_path

    def detect_input_files(self, input_dir: str = "tableau/input") -> list:
        """
        Detect all Tableau files in input directory

        Args:
            input_dir: Directory to scan

        Returns:
            List of .twb/.twbx file paths
        """
        files = []

        if not os.path.exists(input_dir):
            return files

        for file in os.listdir(input_dir):
            if file.endswith('.twb') or file.endswith('.twbx'):
                files.append(os.path.join(input_dir, file))

        return files

    def list_templates(self) -> None:
        """List available templates"""
        templates = self.loader.list_templates()

        print("\nAvailable Templates:")
        print("-" * 60)

        if not templates:
            print("  (No templates found in tableau/templates/)")
            return

        for tmpl in templates:
            print(f"\n  {tmpl['name']}")
            print(f"    File: {Path(tmpl['path']).name}")
            if tmpl['description']:
                print(f"    Description: {tmpl['description']}")
            if tmpl['use_case']:
                print(f"    Use Case: {tmpl['use_case']}")

        print()


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("TABLEAU DASHBOARD STYLER")
    print("="*60)

    app = TableauStylerApp()

    # Detect input files
    input_files = app.detect_input_files()

    if not input_files:
        print("\n⚠ No Tableau files found in tableau/input/")
        print("\nPlease add .twb or .twbx files to tableau/input/ directory")
        return 1

    print(f"\nFound {len(input_files)} file(s) to process:")
    for file in input_files:
        print(f"  - {Path(file).name}")

    # Process each file
    results = []
    for input_file in input_files:
        try:
            output_path = app.style_dashboard(
                input_file,
                template_file="corporate_brand.yaml"
            )
            results.append((input_file, output_path, True))
        except Exception as e:
            print(f"\n✗ FAILED: {e}\n")
            results.append((input_file, None, False))

    # Final summary
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)

    success_count = sum(1 for _, _, success in results if success)
    fail_count = len(results) - success_count

    for input_file, output_path, success in results:
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{status}: {Path(input_file).name}")

    print(f"\n{success_count} succeeded, {fail_count} failed")
    print("="*60 + "\n")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
