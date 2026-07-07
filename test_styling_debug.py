"""
Debug script to test if styling is actually being applied
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from parser.tableau_parser import TableauParser
from config.template_loader import TemplateLoader
from styling.engine import StylingEngine
from lxml import etree

# Parse workbook
parser = TableauParser()
workbook = parser.parse("tableau/input/RE - NO - Kraken - Competitor Analysis Hjem.twbx")

print("Original workbook:")
print(f"  XML root: {workbook.xml_root}")
print(f"  Dashboards: {len(workbook.dashboards)}")
print(f"  Worksheets: {len(workbook.worksheets)}")

# Find a color map in original
original_xml_str = etree.tostring(workbook.xml_root, encoding='unicode')
print(f"\nOriginal XML contains '#4e79a7': {('#4e79a7' in original_xml_str)}")
print(f"Original XML contains '#7E2D25': {('#7E2D25' in original_xml_str)}")

# Load template
loader = TemplateLoader()
template = loader.load("corporate_brand.yaml")
print(f"\nTemplate categorical colors: {template.colors.categorical[:3]}")

# Apply styling
engine = StylingEngine()
styled_workbook = engine.apply_template(workbook, template)

print(f"\nStyled workbook:")
print(f"  XML root: {styled_workbook.xml_root}")
print(f"  Same object as original? {styled_workbook.xml_root is workbook.xml_root}")

# Check styled XML
styled_xml_str = etree.tostring(styled_workbook.xml_root, encoding='unicode')
print(f"\nStyled XML contains '#4e79a7': {('#4e79a7' in styled_xml_str)}")
print(f"Styled XML contains '#7E2D25': {('#7E2D25' in styled_xml_str)}")
print(f"Styled XML contains '#34A83A': {('#34A83A' in styled_xml_str)}")

# Check if gridline rule was added
print(f"\nStyled XML contains 'gridline': {('gridline' in styled_xml_str)}")

# Show a sample of modified XML
if '#7E2D25' in styled_xml_str:
    print("\n✓ SUCCESS: Template colors found in styled XML!")
    idx = styled_xml_str.find('#7E2D25')
    print(f"Context: ...{styled_xml_str[max(0,idx-100):idx+100]}...")
else:
    print("\n✗ FAIL: Template colors NOT found in styled XML")
    print("This means our transformations aren't working!")
