# TICKET-0008

## Type
Enhancement

## Status
Open

## Created
2026-07-07

## Title
Enhance Styling Engine for Comprehensive Chart and Layout Transformation

## Description
The current styling engine applies basic background colors and typography, but doesn't comprehensively transform Tableau dashboards. Need to enhance the engine to:

1. **Apply template colors to actual chart marks** (bars, lines, shapes)
2. **Improve whitespace and padding** throughout dashboards
3. **Standardize spacing** between elements
4. **Apply colors to chart-specific style-rules** and encodings

**Current State:**
- ✅ Dashboard/worksheet backgrounds
- ✅ Basic typography (partially)
- ✅ Color palette defined in preferences
- ❌ Chart mark colors not applied
- ❌ Grid lines, axes not styled
- ❌ Spacing/padding not standardized
- ❌ Chart-level style-rules not modified

**Expected State:**
- ✅ Charts use burgundy (#7E2D25) and green (#34A83A) from template
- ✅ Consistent padding (12px dashboard, 8px containers)
- ✅ Improved whitespace between elements
- ✅ Grid lines styled (color, opacity from template)
- ✅ Axes styled with template colors
- ✅ All visual elements follow corporate brand

## Parent Ticket
None

## Dependencies
None (enhancement of existing system)

## Implementation Plan

### Phase 1: Chart Color Application
* [ ] Analyze Tableau `<style-rule>` and `<encoding>` XML structure
* [ ] Update color_transformer to modify chart mark colors
* [ ] Apply categorical palette to dimension-based charts
* [ ] Apply brand colors (burgundy/green) to key metrics
* [ ] Test with bar charts, line charts, pie charts

### Phase 2: Grid Lines and Axes
* [ ] Find and modify gridline style-rules
* [ ] Apply template gridline color and opacity
* [ ] Style axis lines with template colors
* [ ] Update axis label fonts and colors
* [ ] Apply zero-line styling

### Phase 3: Spacing and Padding
* [ ] Traverse all zone elements
* [ ] Apply consistent padding values
* [ ] Standardize spacing between dashboard elements
* [ ] Improve container margins
* [ ] Add whitespace for better visual hierarchy

### Phase 4: Advanced Chart Styling
* [ ] Apply formatting to tooltips
* [ ] Style reference lines
* [ ] Update legend formatting
* [ ] Apply border styles consistently
* [ ] Handle null/missing data colors

### Phase 5: Testing and Validation
* [ ] Test with actual dashboard (Hjem.no, Hybel.no)
* [ ] Verify all charts have brand colors
* [ ] Check spacing and padding consistency
* [ ] Validate output opens in Tableau Desktop
* [ ] Visual comparison before/after

## Technical Details

**Tableau XML Structures to Modify:**

```xml
<!-- Chart mark colors -->
<style-rule element='mark'>
  <encoding attr='color' field='[field]' type='palette'>
    <map to='#7E2D25'>  <!-- Apply burgundy -->

<!-- Grid lines -->
<style-rule element='grid'>
  <format attr='stroke-color' value='#D9D9D9' />
  <format attr='stroke-opacity' value='0.3' />

<!-- Axes -->
<style-rule element='axis'>
  <format attr='stroke-color' value='#6B6B6B' />

<!-- Padding on zones -->
<zone padding='12' ...>
```

## Files to Modify

* `src/styling/color_transformer.py` - Enhanced chart color application
* `src/styling/layout_transformer.py` - Better spacing/padding logic
* `src/styling/chart_styler.py` (new) - Chart-specific styling
* `tableau/templates/corporate_brand.yaml` - Verify all settings present

## Testing Strategy

1. Run styler on RE - NO - Kraken dashboard
2. Open styled.twbx in Tableau Desktop
3. Verify:
   - Charts use burgundy/green colors
   - Padding is consistent (12px/8px)
   - Grid lines are light gray with opacity
   - Whitespace looks professional
   - Overall appearance matches brand

## Success Criteria

✅ Chart bars/lines use template colors (burgundy #7E2D25, green #34A83A)
✅ Grid lines styled with #D9D9D9 at 30% opacity
✅ Axes use #6B6B6B color
✅ Dashboard padding is 12px
✅ Container padding is 8px
✅ Spacing between elements is consistent
✅ Whitespace improves visual hierarchy
✅ Dashboard looks polished and professional
✅ All styling follows corporate_brand.yaml template

## Notes

This is a critical enhancement to make the styler truly useful. The current implementation is a proof-of-concept that successfully parses and writes files, but doesn't comprehensively apply the template.

Target: Make the styled dashboard visually distinct and brand-aligned when opened in Tableau.

## Estimated Complexity
High - Requires deep understanding of Tableau XML structure and extensive testing
