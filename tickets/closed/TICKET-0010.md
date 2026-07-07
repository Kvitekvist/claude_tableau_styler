# TICKET-0010

## Type
Feature

## Status
Open

## Created
2026-07-07

## Title
Build Main Application Orchestrator

## Description
Create the main application entry point that orchestrates the complete styling workflow: detect input files, load template, parse workbook, apply styling, create backup, write output. This is the user-facing command-line application that ties all components together.

## Parent Ticket
TICKET-0005

## Dependencies
- TICKET-0006 (parser)
- TICKET-0007 (config loader)
- TICKET-0008 (styling engine)
- TICKET-0009 (file manager)

## Implementation Plan

### 1. Create Main Application
* Create `src/main.py`
* Create `src/cli.py` (command-line interface)
* Create `tests/test_main.py`

### 2. Implement File Detection
* Scan `tableau/input/` for .twb and .twbx files
* Display available files to user
* Allow selection of file to style (or process all)

### 3. Implement Template Selection
* Scan `tableau/templates/` for .yaml files
* Display available templates with metadata
* Allow selection of template
* Default to `corporate_brand.yaml`

### 4. Implement Main Workflow
```
1. Detect input files
2. Select template (or use default)
3. For each file:
   a. Parse workbook
   b. Load template configuration
   c. Apply styling transformations
   d. Create backup
   e. Write styled output
   f. Report results
4. Display summary (success/failures)
```

### 5. Add Progress Reporting
* Show current step (Parsing... Styling... Writing...)
* Display progress for multiple files
* Show success/error messages
* Provide clear output paths

### 6. Implement Error Handling
* Graceful handling of parse errors
* Handle invalid templates
* Handle file write failures
* Provide actionable error messages
* Don't crash on single file failure (continue with next)

### 7. Add Command-Line Interface
```bash
# Basic usage (process all files with default template)
python src/main.py

# Specify file and template
python src/main.py --file "dashboard.twbx" --template "corporate_brand.yaml"

# Process all files with specific template
python src/main.py --template "dark_mode.yaml"

# Verbose output
python src/main.py --verbose
```

### 8. Testing
* Test single file processing
* Test batch processing (multiple files)
* Test with different templates
* Test error scenarios (missing files, invalid template)
* Integration test: full workflow with real file
* Verify backups created correctly
* Verify output files valid

## Technical Details

**Main Workflow:**
```python
def style_dashboard(input_file: str, template_file: str) -> str:
    print(f"Processing: {input_file}")
    
    # Parse
    print("  → Parsing workbook...")
    parser = TableauParser()
    workbook = parser.parse(input_file)
    
    # Load template
    print("  → Loading template...")
    loader = TemplateLoader()
    template = loader.load(template_file)
    
    # Apply styling
    print("  → Applying styling...")
    engine = StylingEngine()
    styled_workbook = engine.apply_template(workbook, template)
    
    # Save
    print("  → Creating backup...")
    manager = FileManager()
    manager.create_backup(input_file)
    
    print("  → Writing styled output...")
    output_path = manager.write(styled_workbook, input_file, "tableau/output")
    
    print(f"  ✓ Complete: {output_path}")
    return output_path
```

**CLI Arguments:**
```python
parser = argparse.ArgumentParser(
    description="Tableau Dashboard Styler - Apply professional styling to dashboards"
)
parser.add_argument("--file", help="Specific .twb/.twbx file to style")
parser.add_argument("--template", default="corporate_brand.yaml", help="Style template")
parser.add_argument("--verbose", action="store_true", help="Verbose output")
parser.add_argument("--batch", action="store_true", help="Process all files in input/")
```

## Testing Strategy

```python
def test_main_workflow():
    # Integration test
    result = style_dashboard(
        "tableau/input/sample.twbx",
        "tableau/templates/corporate_brand.yaml"
    )
    
    assert os.path.exists(result)
    assert "_styled" in result
    
    # Verify backup created
    backups = os.listdir("tableau/backups")
    assert any("sample_backup_" in b for b in backups)

def test_batch_processing():
    # Place multiple files in input/
    results = main(["--batch", "--template", "corporate_brand.yaml"])
    
    assert len(results) > 0
    assert all(os.path.exists(r) for r in results)

def test_error_handling():
    # Test with invalid file
    with pytest.raises(InvalidTableauFileError):
        style_dashboard("invalid.txt", "corporate_brand.yaml")
```

## Success Criteria

✅ Detects all files in `tableau/input/`
✅ Lists available templates
✅ Successfully processes the provided .twbx file
✅ Applies corporate_brand.yaml template
✅ Creates backup in `tableau/backups/`
✅ Writes styled output to `tableau/output/`
✅ Provides clear progress messages
✅ Handles errors gracefully with helpful messages
✅ Command-line interface works as expected
✅ Integration test passes with real file
✅ Output file opens in Tableau Desktop successfully
✅ Dashboard looks professional and brand-aligned

## User Acceptance Test

**Manual Verification:**
1. Run `python src/main.py`
2. Observe styled output file created
3. Open `tableau/output/RE - NO - Kraken - Competitor Analysis Hjem_styled.twbx` in Tableau Desktop
4. Verify:
   - Colors match corporate brand (burgundy, green)
   - Fonts are Arial with correct sizes
   - Backgrounds are white/light gray
   - Charts look professional and polished
   - Dashboard still functions (filters work, data displays correctly)
5. Compare with original (from backup) to see improvements

## Notes

This is the **final integration** - all components come together here.

Focus on **user experience**:
- Clear messages
- Helpful errors
- Progress indication
- Professional output

If anything fails, provide enough information for the user to fix it (e.g., "Template 'missing.yaml' not found in tableau/templates/")

## Estimated Complexity
Medium - Integration and orchestration with good UX
