# TICKET-0007

## Type
Feature

## Status
Open

## Created
2026-07-07

## Title
Build YAML Template Configuration Loader

## Description
Create a configuration loader that reads YAML style template files (like corporate_brand.yaml), validates the structure, and converts them into Python objects that the styling engine can use. Handle missing fields, provide defaults, and validate color codes and typography settings.

## Parent Ticket
TICKET-0005

## Dependencies
None (can run parallel with TICKET-0006)

## Implementation Plan

### 1. Create Config Module Structure
* Create `src/config/template_loader.py`
* Create `src/config/style_config.py` (data models)
* Create `tests/config/test_template_loader.py`

### 2. Implement YAML Parser
* Load YAML file with PyYAML
* Validate required sections exist
* Provide sensible defaults for optional fields
* Raise clear errors for malformed templates

### 3. Create Configuration Data Models
* `StyleTemplate` - root configuration object
* `ColorPalette` - categorical, sequential, diverging palettes
* `Typography` - font settings for various elements
* `LayoutConfig` - spacing, padding, backgrounds
* `ChartElementConfig` - gridlines, axes, borders
* `ChartTypeConfig` - specific settings per chart type

### 4. Add Validation
* Validate hex color codes (#RRGGBB format)
* Validate font sizes (reasonable range 6-72pt)
* Validate opacity values (0.0 to 1.0)
* Validate required fields are present
* Provide helpful error messages for invalid values

### 5. Implement Template Discovery
* Scan `tableau/templates/` directory
* List all available .yaml templates
* Provide template metadata (name, description, use case)

### 6. Testing
* Test loading corporate_brand.yaml
* Test invalid YAML (syntax errors)
* Test missing required fields
* Test invalid color codes
* Test template discovery

## Technical Details

**YAML Structure Validation:**
```python
required_sections = [
    'metadata',
    'colors',
    'typography',
    'layout',
    'chart_elements'
]
```

**Color Validation:**
```python
def validate_hex_color(color: str) -> bool:
    pattern = r'^#[0-9A-Fa-f]{6}$'
    return re.match(pattern, color) is not None
```

## Testing Strategy

```python
def test_load_corporate_template():
    loader = TemplateLoader()
    template = loader.load("tableau/templates/corporate_brand.yaml")
    
    assert template.metadata.name == "Corporate Brand"
    assert len(template.colors.categorical) == 8
    assert template.colors.brand.primary_burgundy == "#7E2D25"
    assert template.typography.title.font_size == 20

def test_invalid_color_code():
    loader = TemplateLoader()
    with pytest.raises(InvalidColorCodeError):
        loader.load("invalid_template.yaml")  # contains "#ZZZ"
```

## Success Criteria

✅ Loads corporate_brand.yaml successfully
✅ Validates all color codes are valid hex
✅ Validates font sizes are reasonable
✅ Provides clear error messages for invalid templates
✅ Returns usable Python configuration objects
✅ Can list all available templates in directory
✅ Unit tests pass for valid and invalid inputs

## Notes

This module should be **pure configuration loading** - no file system modifications, no styling logic. Just read and validate YAML → Python objects.

Provide helpful defaults so templates don't need to specify every single field.

## Estimated Complexity
Low-Medium - YAML parsing with validation
