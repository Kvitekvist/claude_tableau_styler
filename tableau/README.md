# Tableau Files Directory

This directory contains Tableau workbook files for styling operations.

## Directory Structure

### `input/`
Place your original Tableau workbook files here (.twb or .twbx) that you want to style.

**Example:**
```
tableau/input/
  ├── sales_dashboard.twb
  ├── quarterly_report.twbx
  └── customer_analytics.twb
```

### `output/`
Styled Tableau files will be saved here after processing.

The application will generate output files with naming pattern:
- `{original_name}_styled.twb`
- `{original_name}_styled.twbx`

### `backups/`
Automatic backups of original files before any modifications.

Files are timestamped: `{original_name}_backup_{timestamp}.twb`

### `templates/`
Store reusable style configuration files (JSON/YAML) here.

**Example:**
```
tableau/templates/
  ├── corporate_brand.yaml
  ├── dark_theme.yaml
  └── minimal_clean.yaml
```

## Workflow

1. **Add files** - Copy your Tableau workbooks to `input/`
2. **Run application** - The app will detect files in `input/`
3. **Select & style** - Choose files and apply styling
4. **Automatic backup** - Original backed up to `backups/`
5. **Get output** - Styled files saved to `output/`

## .gitignore

Tableau files in `input/`, `output/`, and `backups/` are ignored by Git to prevent committing large workbooks to version control. Only `templates/` is tracked.
