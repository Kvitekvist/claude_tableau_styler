"""
Test if color replacement is working
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from parser.tableau_parser import TableauParser
from config.template_loader import TemplateLoader
from styling.color_transformer import ColorTransformer
from lxml import etree

# Parse workbook
parser = TableauParser()
workbook = parser.parse("tableau/input/RE - NO - Kraken - Competitor Analysis Hjem.twbx")

# Load template
loader = TemplateLoader()
template = loader.load("corporate_brand.yaml")

print(f"Template colors: {template.colors.categorical[:3]}")

# Check original colors
original_xml = etree.tostring(workbook.xml_root, encoding='unicode')
print(f"\nOriginal has #4e79a7: {('#4e79a7' in original_xml)}")
print(f"Original has #7E2D25: {('#7E2D25' in original_xml)}")

# Find worksheets and style rules
worksheets = workbook.xml_root.findall('.//worksheet')
print(f"\nFound {len(worksheets)} worksheets")

mark_rules = workbook.xml_root.findall('.//style-rule[@element="mark"]')
print(f"Found {len(mark_rules)} mark style rules")

for i, rule in enumerate(mark_rules[:3]):
    encodings = rule.findall('.//encoding[@attr="color"]')
    print(f"\nMark rule {i}: {len(encodings)} color encodings")
    for enc in encodings:
        maps = enc.findall('map')
        print(f"  - {len(maps)} color maps")
        for m in maps[:2]:
            print(f"    Current: {m.get('to')}")

# Apply color transformer
transformer = ColorTransformer()
transformer.apply(workbook, template)

# Check styled colors
styled_xml = etree.tostring(workbook.xml_root, encoding='unicode')
print(f"\nAfter styling has #4e79a7: {('#4e79a7' in styled_xml)}")
print(f"After styling has #7E2D25: {('#7E2D25' in styled_xml)}")

# Check the same rules again
for i, rule in enumerate(mark_rules[:3]):
    encodings = rule.findall('.//encoding[@attr="color"]')
    for enc in encodings:
        maps = enc.findall('map')
        print(f"\nAfter transformation, map colors:")
        for m in maps[:2]:
            print(f"  - {m.get('to')}")
