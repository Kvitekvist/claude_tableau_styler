# Style Templates

This directory contains reusable style configuration templates for Tableau Dashboard Styler.

## Available Templates

### **corporate_brand.yaml**
Primary corporate brand styling using burgundy and green accent colors.

**Use for:**
- Executive dashboards
- Client-facing reports
- Presentation materials
- Board-level analytics

**Key Features:**
- Brand-aligned color palettes (categorical, sequential, diverging)
- Professional typography settings
- Semantic colors for KPIs (success/warning/danger)
- Optimized for both screen and print

## Template Structure

Each template is a YAML file with these sections:

### 1. **Metadata**
Template information (name, description, version, use case)

### 2. **Colors**
- **Brand Colors** - Your primary brand identity
- **Neutrals** - Text and background colors
- **Categorical Palette** - For dimensions (8 colors)
- **Sequential Palette** - For continuous measures (5 shades)
- **Diverging Palette** - For variance analysis (negative ↔ positive)
- **Semantic Colors** - Success, warning, danger, info

### 3. **Typography**
Font settings for:
- Dashboard titles
- Sheet titles
- Body text
- Axis labels
- Data labels
- Tooltips

### 4. **Layout**
- Dashboard backgrounds and padding
- Container styling and spacing
- Sheet backgrounds and borders

### 5. **Chart Elements**
- Grid lines (color, opacity, style)
- Axis styling
- Reference lines
- Borders and shadows
- Null value handling

### 6. **Chart Types**
Specific settings for:
- Bar charts
- Line charts
- Pie charts
- Maps
- Heat maps
- KPI cards

### 7. **Filters**
Filter control styling

### 8. **Rules**
Application rules and quality settings

## Creating Your Own Template

1. **Copy an existing template** as a starting point
2. **Edit the colors** section with your brand palette
3. **Adjust typography** to match your brand fonts
4. **Modify layout** spacing and backgrounds
5. **Save with descriptive name** (e.g., `client_name_theme.yaml`)

## Tips for Great Templates

### Color Palettes

**Categorical (8 colors):**
- Use distinct, easily distinguishable colors
- Order by importance (most important first)
- Ensure sufficient contrast between adjacent colors

**Sequential (5 shades):**
- Light to dark progression
- Single hue or analogous hues
- Use for heat maps, filled maps, intensity charts

**Diverging (5 colors):**
- Two opposing colors with neutral center
- Use for above/below comparisons
- Examples: red ↔ gray ↔ green, blue ↔ white ↔ orange

### Typography

- **Limit to 2 font families** maximum
- **Use clear hierarchy** (title > subtitle > body)
- **Ensure readability** (11pt minimum for body text)
- **Test on projection** if used for presentations

### Accessibility

- **Color contrast ratio** minimum 4.5:1 for text
- **Don't rely solely on color** - use patterns/shapes too
- **Colorblind-friendly** palettes (test with simulators)
- **Large enough text** for readability

## Example: Creating a Dark Theme

```yaml
metadata:
  name: "Dark Mode Professional"
  description: "Low-light friendly dark theme"

colors:
  neutrals:
    background: "#1E1E1E"      # Dark background
    text: "#E0E0E0"            # Light text
    borders: "#3C3C3C"         # Subtle borders
  
  categorical:
    - "#4FC3F7"  # Bright blue
    - "#81C784"  # Green
    - "#FFB74D"  # Orange
    # ... more colors

typography:
  title:
    color: "#FFFFFF"           # White for dark backgrounds
    font_size: 22

layout:
  dashboard:
    background_color: "#1E1E1E"  # Dark
  
chart_elements:
  gridlines:
    color: "#3C3C3C"           # Subtle grids
    opacity: 0.2
```

## Template Validation

Before using a template, verify:

- [ ] All color codes are valid hex (#RRGGBB)
- [ ] Font sizes are reasonable (8-24pt typically)
- [ ] Opacity values are 0.0 to 1.0
- [ ] Required sections are present
- [ ] Colors have sufficient contrast

## Next Steps

Once templates are created, the Tableau Dashboard Styler application will:

1. Auto-detect templates in this directory
2. Let you preview templates
3. Apply selected template to dashboards
4. Generate before/after comparisons
