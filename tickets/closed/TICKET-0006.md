# TICKET-0003

## Type
Feature

## Status
Open

## Created
2026-07-07

## Title
Build File Manager (Backup, Read, Write)

## Description
Create a safe file manager that handles all file I/O operations: reading original Tableau files, creating automatic timestamped backups, and writing styled outputs. Support both .twb (uncompressed XML) and .twbx (compressed zip) formats with robust error handling.

## Parent Ticket
TICKET-0002

## Dependencies
- TICKET-0003 (requires parser to read files)
- TICKET-0005 (requires styled workbook object to write)

## Implementation Plan

### 1. Create File Manager Module
* Create `src/utils/file_manager.py`
* Create `tests/utils/test_file_manager.py`

### 2. Implement Backup System
* Generate timestamped backup filenames (e.g., `dashboard_backup_20260707_143022.twbx`)
* Copy original file to `tableau/backups/` before any modification
* Verify backup was created successfully
* Handle backup failures gracefully (abort operation if backup fails)

### 3. Implement .twb Writer
* Convert styled workbook object back to XML
* Write XML with proper formatting (pretty print)
* Preserve XML declaration and namespaces
* Validate XML structure before writing

### 4. Implement .twbx Writer
* Create temporary directory
* Write .twb XML file
* Copy any data extracts from original (if present)
* Compress into .twbx zip archive
* Clean up temporary files
* Validate zip integrity

### 5. Implement Safe Write Operations
* Write to temporary file first
* Validate written file can be parsed
* Only then move to final location
* Rollback on any errors

### 6. Add Output Naming
* Generate output filenames: `{original_name}_styled.{ext}`
* Save to `tableau/output/` directory
* Handle filename collisions (append number if exists)
* Return output file path

### 7. Testing
* Test backup creation
* Test .twb writing
* Test .twbx writing (zip creation)
* Test error handling (disk full, permissions, invalid paths)
* Test rollback on failure
* Verify output files are valid Tableau workbooks

## Technical Details

**Backup Strategy:**
```python
def create_backup(original_path: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = Path(original_path).stem
    extension = Path(original_path).suffix
    backup_path = f"tableau/backups/{filename}_backup_{timestamp}{extension}"
    shutil.copy2(original_path, backup_path)
    return backup_path
```

**Safe Write Pattern:**
```python
def safe_write(workbook, output_path):
    temp_path = output_path + ".tmp"
    try:
        write_to_file(workbook, temp_path)
        validate_file(temp_path)  # Ensure it's valid
        shutil.move(temp_path, output_path)
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise
```

**ZIP Structure for .twbx:**
```
dashboard.twbx (zip file)
├── dashboard.twb (main XML)
└── Data/
    └── Extracts/ (optional data extracts - preserve from original)
```

## Testing Strategy

```python
def test_create_backup():
    manager = FileManager()
    original = "tableau/input/sample.twbx"
    backup_path = manager.create_backup(original)
    
    assert os.path.exists(backup_path)
    assert "backup_" in backup_path
    assert filecmp.cmp(original, backup_path)  # Exact copy

def test_write_styled_twbx():
    manager = FileManager()
    styled_workbook = create_styled_workbook()
    
    output_path = manager.write(
        styled_workbook,
        original_path="tableau/input/dashboard.twbx",
        output_dir="tableau/output"
    )
    
    assert os.path.exists(output_path)
    assert output_path.endswith("_styled.twbx")
    
    # Verify it's a valid Tableau file
    parser = TableauParser()
    workbook = parser.parse(output_path)
    assert workbook is not None

def test_backup_failure_aborts():
    manager = FileManager()
    
    with pytest.raises(BackupFailedError):
        # Simulate disk full or permissions error
        manager.write(workbook, "/readonly/path.twbx")
```

## Success Criteria

✅ Creates timestamped backups before modification
✅ Writes .twb files (uncompressed XML)
✅ Writes .twbx files (compressed zip with correct structure)
✅ Generates appropriate output filenames (_styled suffix)
✅ Handles file collisions (appends number if file exists)
✅ Validates written files are parseable
✅ Rolls back on errors (doesn't leave corrupted files)
✅ Preserves data extracts in .twbx files
✅ Unit tests pass for all scenarios
✅ Integration test: backup → write → verify cycle works

## Notes

**Safety is paramount**:
- ALWAYS create backup before any modification
- ALWAYS validate written files
- NEVER overwrite original files
- ALWAYS clean up temporary files

If backup fails, the entire operation must abort - better to fail safely than risk data loss.

Preserve the complete structure of .twbx files, including any embedded data extracts.

## Estimated Complexity
Medium - File I/O with zip handling and safety mechanisms
