# TICKET-0005

## Type
Feature (Parent)

## Status
Open

## Created
2026-07-07

## Title
Complete Tableau Dashboard Styling System

## Description
Build the complete end-to-end system to apply the corporate brand template to Tableau workbook files. This involves parsing .twb/.twbx files, loading YAML style templates, applying styling transformations to dashboard XML, and safely writing styled outputs with backups.

**User Request**: "Use this [corporate_brand.yaml] to style up my tableau report to make it look professional and sharp"

**Input File**: `tableau/input/RE - NO - Kraken - Competitor Analysis Hjem.twbx`

**Template**: `tableau/templates/corporate_brand.yaml`

**Expected Output**: `tableau/output/RE - NO - Kraken - Competitor Analysis Hjem_styled.twbx`

## Child Tickets

This is broken into 5 sequential child tickets:

- TICKET-0006: Tableau file parser (.twb/.twbx reader)
- TICKET-0007: YAML template configuration loader
- TICKET-0008: Core styling engine (color/font/layout transformer)
- TICKET-0009: File manager (backup, read, write operations)
- TICKET-0010: Main application orchestrator

## Dependencies

None (parent ticket)

## Implementation Plan

### Phase 1: Foundation (TICKET-0006, TICKET-0007)
* [x] Parse .twbx (extract XML from zip)
* [x] Parse .twb (XML structure analysis)
* [x] Load and validate YAML template
* [x] Build internal configuration model

### Phase 2: Core Engine (TICKET-0008)
* [ ] Apply color palettes (categorical, sequential, diverging)
* [ ] Transform typography (fonts, sizes, colors)
* [ ] Modify layout properties (padding, spacing, backgrounds)
* [ ] Update chart elements (gridlines, axes, borders)
* [ ] Handle specific chart types (bar, line, pie, maps)

### Phase 3: Integration (TICKET-0009, TICKET-0010)
* [ ] Implement safe backup mechanism
* [ ] Write modified XML back to .twb/.twbx
* [ ] Build main application flow
* [ ] Add error handling and validation
* [ ] Test with actual dashboard file

## Testing Strategy

1. **Unit Tests**: Each component tested independently
2. **Integration Tests**: End-to-end workflow with sample file
3. **Visual Validation**: Compare before/after dashboard screenshots
4. **Safety Tests**: Verify backups created, original preserved

## Success Criteria

✅ Successfully parse the provided .twbx file
✅ Load corporate_brand.yaml template
✅ Apply burgundy/green brand colors to charts
✅ Update fonts to Arial with specified sizes
✅ Modify backgrounds, borders, and spacing
✅ Create automatic backup before modification
✅ Output styled .twbx file that opens in Tableau
✅ Dashboard looks professional and brand-aligned

## Notes

This is a comprehensive feature requiring careful XML manipulation. Each child ticket builds on the previous one, ensuring we can test at each stage before moving forward.

The styling engine must preserve:
- Data connections
- Calculated fields
- Dashboard interactivity
- Filter functionality

## Parent Ticket
None

## Child Tickets
- TICKET-0006
- TICKET-0007
- TICKET-0008
- TICKET-0009
- TICKET-0010

## Dependencies
None
