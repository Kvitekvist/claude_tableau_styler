# TICKET-0008

## Type
Feature

## Status
Open

## Created
2026-07-07

## Title
Build Core Styling Engine

## Description
Create the styling engine that takes a parsed Tableau workbook (from TICKET-0006) and a style template (from TICKET-0007), then applies the styling transformations to the workbook's XML structure. This includes modifying colors, fonts, layouts, and chart properties while preserving data connections and calculations.

## Parent Ticket
TICKET-0005

## Dependencies
- TICKET-0006 (requires parsed workbook object)
- TICKET-0007 (requires style configuration object)

## Implementation Plan

### 1. Create Styling Module Structure
* Create `src/styling/engine.py`
* Create `src/styling/color_transformer.py`
* Create `src/styling/typography_transformer.py`
* Create `src/styling/layout_transformer.py`
* Create `tests/styling/test_engine.py`

### 2. Implement Color Transformation
* Apply categorical palette to dimension-based charts
* Apply sequential palette to continuous measures
* Apply diverging palette to variance/comparison charts
* Update background colors (dashboard, sheets, containers)
* Update border colors
* Update text colors
* Preserve explicit color legends when specified

### 3. Implement Typography Transformation
* Update dashboard title fonts (family, size, weight, color)
* Update sheet title fonts
* Update body text/labels
* Update axis label fonts
* Update data label fonts
* Update tooltip fonts

### 4. Implement Layout Transformation
* Update dashboard padding/margins
* Update container backgrounds and spacing
* Update sheet backgrounds and borders
* Update title backgrounds

### 5. Implement Chart Element Transformation
* Update gridline color, style, opacity
* Update axis line colors and widths
* Update reference line styling
* Update border styles
* Configure null value handling

### 6. Implement Chart Type Specific Styling
* Bar charts (colors, borders, palettes)
* Line charts (line width, markers, colors)
* Pie charts (slice colors, borders)
* Maps (base colors, sequential palettes, borders)
* Heat maps (sequential palette, label colors)
* KPI cards (background, number color, trend colors)

### 7. Add Safety Mechanisms
* **Preserve data connections** - don't modify datasource XML
* **Preserve calculated fields** - don't modify calculations
* **Preserve interactivity** - maintain filters, actions, parameters
* Validate XML structure after modifications
* Create deep copy of workbook before modifying

### 8. Testing
* Test color transformation on sample workbook
* Test typography changes
* Test layout modifications
* Test preservation of data connections
* Verify styled XML is valid Tableau format
* Integration test with full template

## Technical Details

**XML Modification Strategy:**
```python
# Example: Update dashboard background color
def apply_dashboard_background(dashboard_xml, color):
    # Find <dashboard> element
    # Locate or create <format> child
    # Update background-color property
    # Preserve all other properties
```

**Preservation Rules:**
- Never modify `<datasources>` section
- Never modify `<column>` calculation formulas
- Never modify `<filter>` or `<parameter>` definitions
- Never modify `<action>` interactivity

**Styling Priority:**
1. Explicit user-defined colors (preserve if template says so)
2. Template-specified colors
3. Tableau defaults (fallback)

## Testing Strategy

```python
def test_apply_brand_colors():
    workbook = parse_workbook("sample.twb")
    template = load_template("corporate_brand.yaml")
    engine = StylingEngine()
    
    styled_workbook = engine.apply_template(workbook, template)
    
    # Verify dashboard background is white
    assert styled_workbook.dashboards[0].background_color == "#FFFFFF"
    
    # Verify title color is burgundy
    assert styled_workbook.dashboards[0].title.color == "#7E2D25"
    
    # Verify data connections preserved
    assert len(styled_workbook.datasources) == len(workbook.datasources)

def test_preserve_calculations():
    # Ensure calculated fields remain unchanged
    assert styled_workbook.get_calculation("Profit Ratio") == workbook.get_calculation("Profit Ratio")
```

## Success Criteria

✅ Applies color palettes correctly (categorical, sequential, diverging)
✅ Updates typography across all text elements
✅ Modifies layout properties (padding, spacing, backgrounds)
✅ Updates chart elements (grids, axes, borders)
✅ Handles chart-type-specific styling
✅ **Preserves data connections** (critical!)
✅ **Preserves calculated fields** (critical!)
✅ **Preserves interactivity** (filters, actions)
✅ Validates modified XML is structurally valid
✅ Unit tests pass for all transformations
✅ Integration test with corporate_brand.yaml succeeds

## Notes

This is the **most complex** component - careful XML manipulation required.

**Safety First**: If uncertain about modifying an XML element, preserve it unchanged. Better to under-style than break the dashboard.

Test incremental changes - start with simple color updates, verify they work, then add more complex transformations.

## Estimated Complexity
High - Complex XML transformations with preservation logic
