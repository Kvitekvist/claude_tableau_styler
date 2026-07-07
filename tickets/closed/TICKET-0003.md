# TICKET-0003

## Type
Feature

## Status
Open

## Created
2026-07-07

## Title
Build Tableau File Parser (.twb/.twbx)

## Description
Create a robust parser that can read both .twb (uncompressed XML) and .twbx (compressed zip containing XML) Tableau workbook files. Extract the XML structure, parse dashboard elements, worksheets, and formatting properties into a usable Python object model.

## Parent Ticket
TICKET-0002

## Dependencies
None (first child ticket)

## Implementation Plan

### 1. Create Parser Module Structure
* Create `src/parser/tableau_parser.py`
* Create `src/parser/workbook.py` (data models)
* Create `tests/parser/test_tableau_parser.py`

### 2. Implement .twbx Handler
* Detect .twbx file format
* Extract zip contents to temporary location
* Locate the .twb XML file inside
* Clean up temporary files after parsing

### 3. Implement .twb XML Parser
* Parse XML using lxml
* Extract workbook structure (dashboards, worksheets)
* Identify formatting elements:
  - Color definitions
  - Font specifications
  - Layout properties
  - Chart configurations
* Build internal object model

### 4. Create Data Models
* `Workbook` class - represents entire workbook
* `Dashboard` class - individual dashboard
* `Worksheet` class - individual worksheet
* `Format` class - styling properties

### 5. Add Validation
* Verify file format (is it a valid Tableau file?)
* Check XML structure
* Handle corrupted or incomplete files gracefully
* Provide meaningful error messages

### 6. Testing
* Test with provided .twbx file
* Test with sample .twb file
* Test error cases (invalid files, corrupted zip, missing XML)
* Verify parsed structure matches expected format

## Technical Details

**File Format Notes:**
- `.twb` = Uncompressed XML file
- `.twbx` = ZIP archive containing .twb + data extracts
- XML namespace: `http://tableau.com/api` (or similar)
- Root element: `<workbook>`

**Key XML Elements to Parse:**
- `<workbook>` - root
- `<dashboards>` - dashboard definitions
- `<worksheets>` - worksheet definitions
- `<datasources>` - data connections (preserve these)
- `<preferences>` - formatting and style properties
- `<style>` - color palettes, fonts

## Testing Strategy

```python
def test_parse_twbx():
    parser = TableauParser()
    workbook = parser.parse("tableau/input/RE - NO - Kraken - Competitor Analysis Hjem.twbx")
    
    assert workbook is not None
    assert len(workbook.dashboards) > 0
    assert workbook.file_type == "twbx"

def test_parse_invalid_file():
    parser = TableauParser()
    with pytest.raises(InvalidTableauFileError):
        parser.parse("invalid.txt")
```

## Success Criteria

✅ Can read .twbx files (extract XML from zip)
✅ Can read .twb files (parse XML directly)
✅ Extracts dashboard and worksheet structures
✅ Identifies current formatting/styling properties
✅ Handles errors gracefully with clear messages
✅ Unit tests pass with provided file
✅ Returns usable Python object model

## Notes

Focus on **reading only** in this ticket. Writing/modification happens in later tickets.

Do NOT modify the original file - this is read-only parsing.

## Estimated Complexity
Medium - XML parsing with zip handling
