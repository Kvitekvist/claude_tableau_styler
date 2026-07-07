"""
Debug the write process
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from parser.tableau_parser import TableauParser
from config.template_loader import TemplateLoader
from styling.engine import StylingEngine
from lxml import etree

# Parse and style
parser = TableauParser()
workbook = parser.parse("tableau/input/RE - NO - Kraken - Competitor Analysis Hjem.twbx")

loader = TemplateLoader()
template = loader.load("corporate_brand.yaml")

engine = StylingEngine()
styled_workbook = engine.apply_template(workbook, template)

# Check styled XML before writing
styled_xml_str = etree.tostring(styled_workbook.xml_root, encoding='unicode')
print(f"Before write - Styled XML contains '#7E2D25': {('#7E2D25' in styled_xml_str)}")

# Write the XML tree directly to a test file
print("\nWriting styled XML to test file...")
# Rebuild tree from modified root
from lxml import etree as et
tree = et.ElementTree(styled_workbook.xml_root)
tree.write(
    "tableau/output/test_manual_write.twb",
    encoding='utf-8',
    xml_declaration=True,
    pretty_print=True
)

# Read it back and check
print("Reading back the written file...")
with open("tableau/output/test_manual_write.twb", 'r', encoding='utf-8') as f:
    written_content = f.read()

print(f"After write - File contains '#7E2D25': {('#7E2D25' in written_content)}")
print(f"After write - File contains '#34A83A': {('#34A83A' in written_content)}")

if '#7E2D25' in written_content:
    print("\nSUCCESS: Colors persist through write!")
else:
    print("\nFAIL: Colors lost during write!")
