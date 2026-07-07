# Dashboard Layout & Design Guidelines

## Objective

Build Tableau dashboards that resemble modern executive BI dashboards (Power BI, Sigma, Looker Studio, modern SaaS analytics), not a collection of individual worksheets.

The dashboard should feel intentionally designed with strong visual hierarchy, generous whitespace, consistent sizing, and perfect alignment.

Analytical correctness and layout quality are equally important.

---

# Core Design Philosophy

Design the dashboard as a complete application.

Every object should have a purpose and belong to a structured layout.

Avoid filling every available space with charts.

Whitespace is a design element.

The user's eye should naturally follow this hierarchy:

1. Dashboard Title
2. Filter Bar
3. KPI Summary Cards
4. Primary Trend Visualization
5. Supporting Analysis Charts
6. Detail Table

---

# Grid System

Always build using a strict grid.

Use a 12-column layout with consistent spacing.

Example layout:

```
--------------------------------------------------
Dashboard Title
--------------------------------------------------

Filter Bar

--------------------------------------------------

KPI 1 | KPI 2 | KPI 3 | KPI 4 | KPI 5

--------------------------------------------------

Primary Trend Chart

--------------------------------------------------

Analysis Chart A      Analysis Chart B

--------------------------------------------------

Detail Table

--------------------------------------------------
```

Never randomly size or position charts.

Every component must align to the same invisible grid.

---

# Tableau Layout Rules

ALWAYS use tiled containers.

Structure:

```
Vertical Container
    Horizontal Filter Container
    Horizontal KPI Container
    Trend Container
    Horizontal Analysis Container
    Table Container
```

Avoid floating objects unless absolutely necessary.

Do not manually position worksheets.

---

# Spacing Rules

Use consistent spacing everywhere.

**Outer dashboard padding**: 24px

**Spacing between sections**: 20–24px

**Spacing between KPI cards**: 16px

**Internal card padding**: 16px

**Chart padding**: 12–16px

Never allow charts to touch each other.

Never allow text to touch borders.

Whitespace should separate every visual section.

---

# KPI Cards

Every KPI belongs inside a card.

Each KPI card should contain:
- Large Metric
- Small Label
- (Optional Icon)

Rules:
• Equal width
• Equal height
• Same typography
• Centered vertically
• Consistent padding
• Light background
• Thin border
• Minimal visual noise

Do NOT resize KPI cards independently.

---

# Section Headers

Every visualization should have:
- Section Title
- (Optional subtitle)
- Chart

Titles should always align with the left edge of the visualization.

Avoid floating text.

---

# Visual Hierarchy

Not every chart deserves equal attention.

Use size to communicate importance.

Example:

**Primary Trend Chart**: Height: ~300px

**Supporting Charts**: Height: ~220px

**Tables**: Only as tall as necessary

The most important visualization should occupy the most space.

---

# Tables

Tables should support the dashboard, not dominate it.

Use:
• Compact row height
• Zebra striping
• Minimal borders
• Left-aligned text
• Limited visible rows
• Consistent typography

Remove unnecessary gridlines.

---

# Typography

Use only a small typography scale.

**Dashboard Title**: 24–30px

**Section Headers**: 16–18px

**Body Text**: 10–12px

**KPI Values**: 28–36px

**Labels**: 11–12px

Do not mix many font sizes.

---

# Alignment Rules

Everything must align.

Left edges should line up.

Charts should have equal heights when side-by-side.

Cards should have identical widths.

Titles should begin at the same x-position.

Do not leave uneven gaps.

The dashboard should appear mathematically aligned.

---

# Color Usage

Follow the provided corporate color palette.

Use:
- Primary Color
- Secondary Accent
- Neutral Gray

Avoid assigning different colors to every chart.

Reserve accent colors for:
• Highlights
• Negative values
• Selected states
• Alerts

Most backgrounds should remain neutral.

---

# Borders & Backgrounds

Use subtle separation.

Recommended:
• White or very light gray card backgrounds
• Thin borders
• Soft shadows only if supported
• Minimal decoration

Avoid heavy outlines.
Avoid thick borders.
Avoid visual clutter.

---

# Chart Design

Charts should emphasize readability.

Guidelines:
• Remove unnecessary gridlines.
• Remove chart borders.
• Reduce excessive axis labels.
• Keep legends compact.
• Prefer direct labels where appropriate.
• Maintain consistent axis formatting.
• Avoid unnecessary chart junk.

Every chart should maximize data-to-ink ratio.

---

# Dashboard Density

Do NOT attempt to maximize the number of charts.

Instead prioritize:
• Readability
• Whitespace
• Visual hierarchy
• Simplicity

It is preferable to leave empty space than to overcrowd the dashboard.

---

# Consistency Rules

Every similar object should look identical.

Examples:

✓ All KPI cards have identical size.
✓ All section titles use the same font.
✓ All charts share consistent padding.
✓ All filters have equal height.
✓ All containers have equal spacing.

Avoid visual inconsistency.

---

# Final Quality Checklist

Before considering the dashboard complete, verify:

✓ Grid-based layout
✓ Perfect alignment
✓ Equal spacing
✓ Consistent padding
✓ Equal KPI sizing
✓ Strong visual hierarchy
✓ Minimal clutter
✓ Clear reading flow
✓ Balanced whitespace
✓ Modern executive dashboard appearance

The finished dashboard should resemble a professionally designed Power BI or modern SaaS analytics dashboard rather than a collection of Tableau worksheets placed onto a canvas.
