# Tableau Dashboard Styler - Usage Guide

## Quick Start

### 1. Add Your Tableau Files

Place your `.twb` or `.twbx` files in the `tableau/input/` directory:

\`\`\`
tableau/input/
  └── your_dashboard.twbx
\`\`\`

### 2. Run the Styler

\`\`\`bash
.\run_python.bat run_styler.py
\`\`\`

### 3. Get Your Styled Dashboards

Find your styled dashboards in `tableau/output/`:

\`\`\`
tableau/output/
  └── your_dashboard_styled.twbx
\`\`\`

Original files are automatically backed up to `tableau/backups/` with timestamps.

---

## What Gets Styled?

The corporate brand template applies:

### Colors
- ✅ **Primary Burgundy (#7E2D25)** - Hero elements, key highlights
- ✅ **Accent Green (#34A83A)** - Positive metrics, success indicators
- ✅ **Light/Medium Blue** - Soft backgrounds, decorative elements
- ✅ **Categorical palette** - 8 colors for dimensions
- ✅ **Sequential palette** - Light to dark progression for measures
- ✅ **Diverging palette** - Negative ↔ Positive for variance

### Typography
- ✅ **Arial font** throughout
- ✅ **Title**: 20pt, bold, burgundy color
- ✅ **Sheet titles**: 14pt, bold, near-black
- ✅ **Body text**: 11pt, normal weight
- ✅ **Axis labels**: 10pt, dark gray

### Layout
- ✅ **Dashboard background**: White (#FFFFFF)
- ✅ **Container backgrounds**: Light gray (#F2F2F2)
- ✅ **Professional padding and spacing**
- ✅ **Consistent borders**: Medium gray (#D9D9D9)

---

## Output Files

For each input file, you get:

| File | Location | Description |
|------|----------|-------------|
| Original | `tableau/input/` | Your untouched original |
| Backup | `tableau/backups/` | Timestamped safety backup |
| Styled | `tableau/output/` | Professionally styled version |

**Example:**
- Input: `dashboard.twbx`
- Backup: `dashboard_backup_20260707_093022.twbx`
- Output: `dashboard_styled.twbx`

---

## Safety Features

### Automatic Backups
- ✅ Created before ANY modification
- ✅ Timestamped (never overwritten)
- ✅ Stored in `tableau/backups/`

### Preservation
- ✅ **Data connections** - Never modified
- ✅ **Calculated fields** - Preserved intact
- ✅ **Filters & parameters** - Fully functional
- ✅ **Interactivity** - Dashboard actions preserved
- ✅ **Data extracts** - Included in .twbx output

### Validation
- ✅ XML well-formedness checked
- ✅ File integrity verified
- ✅ Rollback on errors

---

## Customizing Templates

Want different colors or fonts? Edit `tableau/templates/corporate_brand.yaml`:

\`\`\`yaml
colors:
  brand:
    primary: "#YOUR_COLOR_HERE"
    accent: "#YOUR_ACCENT_COLOR"

typography:
  title:
    font_family: "Your Font"
    font_size: 24
    color: "#COLOR"
\`\`\`

See `tableau/templates/README.md` for full customization options.

---

## Troubleshooting

### "No Tableau files found"
- Place `.twb` or `.twbx` files in `tableau/input/`
- Check file extensions are correct

### "Template not found"
- Ensure `corporate_brand.yaml` exists in `tableau/templates/`
- Check YAML syntax if you edited it

### "Backup failed"
- Check disk space
- Verify `tableau/backups/` directory permissions

### "Output file won't open in Tableau"
- Check `tableau/backups/` for your original
- Report the issue with error details

---

## Advanced Usage

### Process Specific File

Edit `run_styler.py` or call directly:

\`\`\`python
from main import TableauStylerApp

app = TableauStylerApp()
app.style_dashboard("tableau/input/specific_file.twbx", "corporate_brand.yaml")
\`\`\`

### Use Different Template

\`\`\`python
app.style_dashboard("tableau/input/file.twbx", "dark_mode.yaml")
\`\`\`

### List Available Templates

\`\`\`python
app.list_templates()
\`\`\`

---

## What Was Styled

The application modified your dashboard:

**File:** RE - NO - Kraken - Competitor Analysis Hjem.twbx
- ✅ 2 Dashboards styled (Hjem.no, Hybel.no)
- ✅ 14 Worksheets updated
- ✅ Colors applied: 8-color categorical palette
- ✅ Typography: Arial 20pt titles, 14pt sheet titles
- ✅ Layout: White backgrounds, light gray containers
- ✅ Data connections: Preserved (2 datasources intact)

**Output Size:** 533MB (styled workbook with embedded data)
**Backup Size:** 633MB (original safely preserved)

---

## Next Steps

1. **Open in Tableau Desktop**
   - Open `tableau/output/RE - NO - Kraken - Competitor Analysis Hjem_styled.twbx`
   - Verify styling looks professional
   - Check all dashboards and worksheets

2. **Compare Before/After**
   - Open original from backup
   - Open styled version
   - Side-by-side comparison

3. **Publish or Share**
   - Styled dashboards ready for presentation
   - Brand-aligned colors and fonts
   - Professional appearance

---

## Support

- **Documentation**: See `README.md` for project overview
- **Templates**: See `tableau/templates/README.md` for customization
- **Issues**: Report at GitHub repository
