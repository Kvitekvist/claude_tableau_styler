"""
Create Template Dashboard

Creates a properly structured dashboard with empty zones following design guidelines.
User drags worksheets into the zones manually.
"""

import sys
import os

# UTF-8 console support for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from parser.tableau_parser import TableauParser
from lxml import etree
from utils.file_manager import FileManager


def create_empty_zone_structure():
    """Create dashboard XML with empty placeholder zones"""

    dashboard = etree.Element('dashboard')
    dashboard.set('enable-sort-zone-taborder', 'true')
    dashboard.set('name', 'Hjem.no')

    # Title
    layout_options = etree.SubElement(dashboard, 'layout-options')
    title_elem = etree.SubElement(layout_options, 'title')
    formatted_text = etree.SubElement(title_elem, 'formatted-text')

    title_run = etree.SubElement(formatted_text, 'run')
    title_run.set('bold', 'true')
    title_run.set('fontname', 'Arial')
    title_run.set('fontsize', '24')
    title_run.set('fontcolor', '#333333')
    title_run.text = 'Norwegian Real Estate Competitor Analysis'

    br = etree.SubElement(formatted_text, 'run')
    br.set('fontname', 'Arial')
    br.text = '\n'

    subtitle_run = etree.SubElement(formatted_text, 'run')
    subtitle_run.set('fontname', 'Arial')
    subtitle_run.set('fontsize', '14')
    subtitle_run.set('fontcolor', '#6B6B6B')
    subtitle_run.text = 'Drag worksheets into zones below'

    # Style
    style = etree.SubElement(dashboard, 'style')

    # Size
    size = etree.SubElement(dashboard, 'size')
    size.set('maxheight', '1000')
    size.set('maxwidth', '1400')
    size.set('minheight', '1000')
    size.set('minwidth', '1400')
    size.set('sizing-mode', 'fixed')

    # Empty datasources
    datasources = etree.SubElement(dashboard, 'datasources')

    # Zones
    zones = etree.SubElement(dashboard, 'zones')

    # Root container - vertical flow
    root = etree.SubElement(zones, 'zone')
    root.set('h', '952')
    root.set('w', '1352')
    root.set('x', '24')
    root.set('y', '24')
    root.set('id', '1')
    root.set('type-v2', 'layout-flow')
    root.set('param', 'vert')

    zone_id = 2

    # KPI Row - 3 equal cards
    kpi_row = etree.SubElement(root, 'zone')
    kpi_row.set('id', str(zone_id))
    zone_id += 1
    kpi_row.set('type-v2', 'layout-flow')
    kpi_row.set('param', 'horz')
    kpi_row.set('h', '120')
    kpi_row.set('w', '1352')
    kpi_row.set('x', '0')
    kpi_row.set('y', '0')

    # 3 KPI cards
    for i, label in enumerate(['KPI 1: # active ads', 'KPI 2: # Retailers', 'KPI 3: % on FINN']):
        kpi = etree.SubElement(kpi_row, 'zone')
        kpi.set('id', str(zone_id))
        zone_id += 1
        kpi.set('h', '120')
        kpi.set('w', '440')
        kpi.set('x', str(i * 456))
        kpi.set('y', '0')
        kpi.set('type-v2', 'text')  # Text zone for placeholder

        # Add styled card
        zone_style = etree.SubElement(kpi, 'zone-style')
        add_format(zone_style, 'background-color', '#FFFFFF')
        add_format(zone_style, 'border-color', '#E0E0E0')
        add_format(zone_style, 'border-width', '2')
        add_format(zone_style, 'border-style', 'solid')
        add_format(zone_style, 'padding', '16')

        # Add text content
        formatted_text = etree.SubElement(kpi, 'formatted-text')
        run = etree.SubElement(formatted_text, 'run')
        run.set('fontname', 'Arial')
        run.set('fontsize', '11')
        run.set('fontcolor', '#6B6B6B')
        run.set('bold', 'true')
        run.text = f'→ Drag "{label}" here'

    # Primary trend chart
    trend = etree.SubElement(root, 'zone')
    trend.set('id', str(zone_id))
    zone_id += 1
    trend.set('h', '300')
    trend.set('w', '1352')
    trend.set('x', '0')
    trend.set('y', '144')
    trend.set('type-v2', 'text')

    zone_style = etree.SubElement(trend, 'zone-style')
    add_format(zone_style, 'background-color', '#FFFFFF')
    add_format(zone_style, 'border-color', '#E0E0E0')
    add_format(zone_style, 'border-width', '2')
    add_format(zone_style, 'border-style', 'solid')
    add_format(zone_style, 'padding', '16')

    formatted_text = etree.SubElement(trend, 'formatted-text')
    run = etree.SubElement(formatted_text, 'run')
    run.set('fontname', 'Arial')
    run.set('fontsize', '14')
    run.set('fontcolor', '#6B6B6B')
    run.set('bold', 'true')
    run.text = '→ Drag "Hjem.no Daily Active" (area chart) here'

    # Supporting charts row
    support_row = etree.SubElement(root, 'zone')
    support_row.set('id', str(zone_id))
    zone_id += 1
    support_row.set('type-v2', 'layout-flow')
    support_row.set('param', 'horz')
    support_row.set('h', '220')
    support_row.set('w', '1352')
    support_row.set('x', '0')
    support_row.set('y', '468')

    # Bar chart
    bar = etree.SubElement(support_row, 'zone')
    bar.set('id', str(zone_id))
    zone_id += 1
    bar.set('h', '220')
    bar.set('w', '664')
    bar.set('x', '0')
    bar.set('y', '0')
    bar.set('type-v2', 'text')

    zone_style = etree.SubElement(bar, 'zone-style')
    add_format(zone_style, 'background-color', '#FFFFFF')
    add_format(zone_style, 'border-color', '#E0E0E0')
    add_format(zone_style, 'border-width', '2')
    add_format(zone_style, 'border-style', 'solid')
    add_format(zone_style, 'padding', '16')

    formatted_text = etree.SubElement(bar, 'formatted-text')
    run = etree.SubElement(formatted_text, 'run')
    run.set('fontname', 'Arial')
    run.set('fontsize', '11')
    run.set('fontcolor', '#6B6B6B')
    run.set('bold', 'true')
    run.text = '→ Drag "Hjem.no Ads by Agency Group" (bar chart) here'

    # Pie chart
    pie = etree.SubElement(support_row, 'zone')
    pie.set('id', str(zone_id))
    zone_id += 1
    pie.set('h', '220')
    pie.set('w', '664')
    pie.set('x', '688')
    pie.set('y', '0')
    pie.set('type-v2', 'text')

    zone_style = etree.SubElement(pie, 'zone-style')
    add_format(zone_style, 'background-color', '#FFFFFF')
    add_format(zone_style, 'border-color', '#E0E0E0')
    add_format(zone_style, 'border-width', '2')
    add_format(zone_style, 'border-style', 'solid')
    add_format(zone_style, 'padding', '16')

    formatted_text = etree.SubElement(pie, 'formatted-text')
    run = etree.SubElement(formatted_text, 'run')
    run.set('fontname', 'Arial')
    run.set('fontsize', '11')
    run.set('fontcolor', '#6B6B6B')
    run.set('bold', 'true')
    run.text = '→ Drag "Hjem.no Pie Chart" here'

    # Table
    table = etree.SubElement(root, 'zone')
    table.set('id', str(zone_id))
    zone_id += 1
    table.set('h', '200')
    table.set('w', '1352')
    table.set('x', '0')
    table.set('y', '712')
    table.set('type-v2', 'text')

    zone_style = etree.SubElement(table, 'zone-style')
    add_format(zone_style, 'background-color', '#FFFFFF')
    add_format(zone_style, 'border-color', '#E0E0E0')
    add_format(zone_style, 'border-width', '2')
    add_format(zone_style, 'border-style', 'solid')
    add_format(zone_style, 'padding', '16')

    formatted_text = etree.SubElement(table, 'formatted-text')
    run = etree.SubElement(formatted_text, 'run')
    run.set('fontname', 'Arial')
    run.set('fontsize', '11')
    run.set('fontcolor', '#6B6B6B')
    run.set('bold', 'true')
    run.text = '→ Drag "Hjem.no All Ads listed" (table) here'

    # Device layouts
    devicelayouts = etree.SubElement(dashboard, 'devicelayouts')
    phone = etree.SubElement(devicelayouts, 'devicelayout')
    phone.set('auto-generated', 'true')
    phone.set('name', 'Phone')

    phone_layout_options = etree.SubElement(phone, 'layout-options')
    phone_title = etree.SubElement(phone_layout_options, 'title')
    phone_text = etree.SubElement(phone_title, 'formatted-text')
    phone_run = etree.SubElement(phone_text, 'run')
    phone_run.text = 'Template'

    phone_size = etree.SubElement(phone, 'size')
    phone_size.set('maxheight', '2350')
    phone_size.set('minheight', '2350')
    phone_size.set('sizing-mode', 'vscroll')

    phone_zones = etree.SubElement(phone, 'zones')
    phone_root = etree.SubElement(phone_zones, 'zone')
    phone_root.set('h', '100000')
    phone_root.set('id', str(zone_id))
    phone_root.set('type-v2', 'layout-basic')
    phone_root.set('w', '100000')
    phone_root.set('x', '0')
    phone_root.set('y', '0')

    # Simple ID
    simple_id = etree.SubElement(dashboard, 'simple-id')
    simple_id.set('uuid', '{TEMPLATE0-0000-0000-0000-000000000000}')

    return dashboard


def add_format(zone_style, attr, value):
    """Helper to add format element"""
    fmt = etree.SubElement(zone_style, 'format')
    fmt.set('attr', attr)
    fmt.set('value', str(value))


def main():
    print("=" * 60)
    print("TABLEAU TEMPLATE DASHBOARD CREATOR")
    print("=" * 60)
    print()

    input_file = "tableau/input/RE - NO - Kraken - Competitor Analysis Hjem.twbx"
    output_dir = "tableau/output"

    print("→ Parsing original workbook...")
    parser = TableauParser()
    workbook = parser.parse(input_file)
    print(f"  ✓ Parsed {workbook.file_type.upper()}")
    print()

    print("→ Creating template dashboard structure...")
    new_dashboard = create_empty_zone_structure()
    print("  ✓ Dashboard structure created")
    print("    - 3 KPI zones (440px each)")
    print("    - 1 Primary chart zone (300px height)")
    print("    - 2 Supporting chart zones (664px each)")
    print("    - 1 Table zone (200px height)")
    print("    - All zones: white background, subtle borders")
    print("    - 24px outer padding, proper spacing")
    print()

    print("→ Replacing Hjem.no dashboard...")
    dashboards_elem = workbook.xml_root.find('dashboards')
    if dashboards_elem is not None:
        # Remove old Hjem.no
        for dash in dashboards_elem.findall('dashboard'):
            if dash.get('name') == 'Hjem.no':
                dashboards_elem.remove(dash)
        # Add template
        dashboards_elem.append(new_dashboard)
    print("  ✓ Template dashboard added")
    print()

    print("→ Writing template workbook...")
    file_manager = FileManager()
    # Write to specific filename to avoid conflicts
    output_filename = "TEMPLATE - Hjem Dashboard - Drag Worksheets Here.twbx"
    output_path = os.path.join(output_dir, output_filename)

    # Use write method but override the output path
    import shutil
    import tempfile
    import zipfile
    from pathlib import Path

    temp_dir = tempfile.mkdtemp(prefix='tableau_template_')
    try:
        # Write TWB
        twb_path = os.path.join(temp_dir, 'Template.twb')
        tree = etree.ElementTree(workbook.xml_root)
        tree.write(twb_path, encoding='utf-8', xml_declaration=True, pretty_print=True)

        # Copy other content
        if workbook.zip_contents:
            for rel_path, content in workbook.zip_contents.items():
                full_path = os.path.join(temp_dir, rel_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'wb') as f:
                    f.write(content)

        # Create ZIP
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zf.write(file_path, arcname)
    finally:
        shutil.rmtree(temp_dir)

    print(f"  ✓ Output: {output_filename}")
    print()

    print("=" * 60)
    print("✓ TEMPLATE DASHBOARD READY")
    print("=" * 60)
    print()
    print("NEXT STEPS:")
    print()
    print("1. Open in Tableau Desktop:")
    print(f"   {output_path}")
    print()
    print("2. Go to Hjem.no dashboard tab")
    print()
    print("3. Drag these worksheets into the labeled zones:")
    print()
    print("   KPI Row (top):")
    print("   - Zone 1: Drag 'Hjem.no # active ads'")
    print("   - Zone 2: Drag 'Hjem.no # Retailers'")
    print("   - Zone 3: Drag 'Hjem.no % on FINN'")
    print()
    print("   Primary Chart:")
    print("   - Zone 4: Drag 'Hjem.no Daily Active'")
    print()
    print("   Supporting Charts:")
    print("   - Zone 5: Drag 'Hjem.no Ads by Agency Group'")
    print("   - Zone 6: Drag 'Hjem.no Pie Chart'")
    print()
    print("   Table:")
    print("   - Zone 7: Drag 'Hjem.no All Ads listed'")
    print()
    print("4. Save the workbook")
    print()
    print("5. Run: .python/python.exe run_styler.py")
    print("   (This will apply corporate colors & fonts)")
    print()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
