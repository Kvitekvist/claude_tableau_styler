"""
Tests for Tableau Parser
"""

import pytest
import os
from src.parser.tableau_parser import TableauParser, InvalidTableauFileError
from src.parser.workbook import Workbook


class TestTableauParser:
    """Tests for TableauParser"""

    def test_parse_twbx_file(self):
        """Test parsing a real .twbx file"""
        parser = TableauParser()
        file_path = "tableau/input/RE - NO - Kraken - Competitor Analysis Hjem.twbx"

        if not os.path.exists(file_path):
            pytest.skip("Test .twbx file not found")

        workbook = parser.parse(file_path)

        assert workbook is not None
        assert isinstance(workbook, Workbook)
        assert workbook.file_type == 'twbx'
        assert workbook.version is not None
        assert workbook.xml_root is not None
        assert workbook.xml_tree is not None

        # Should have extracted zip contents (images, data)
        assert workbook.zip_contents is not None
        assert len(workbook.zip_contents) > 0

        print(f"\n✓ Parsed {file_path}")
        print(f"  Version: {workbook.version}")
        print(f"  Dashboards: {len(workbook.dashboards)}")
        print(f"  Worksheets: {len(workbook.worksheets)}")
        print(f"  Datasources: {len(workbook.datasources)}")
        print(f"  Zip contents: {len(workbook.zip_contents)} files")

    def test_parse_invalid_file(self):
        """Test parsing an invalid file raises error"""
        parser = TableauParser()

        with pytest.raises(InvalidTableauFileError):
            parser.parse("README.md")  # Not a Tableau file

    def test_parse_nonexistent_file(self):
        """Test parsing nonexistent file raises error"""
        parser = TableauParser()

        with pytest.raises(FileNotFoundError):
            parser.parse("nonexistent.twbx")

    def test_workbook_structure(self):
        """Test that parsed workbook has expected structure"""
        parser = TableauParser()
        file_path = "tableau/input/RE - NO - Kraken - Competitor Analysis Hjem.twbx"

        if not os.path.exists(file_path):
            pytest.skip("Test .twbx file not found")

        workbook = parser.parse(file_path)

        # Should be able to access XML
        assert workbook.xml_root.tag == 'workbook'

        # Should have datasources (they contain data)
        assert len(workbook.datasources) > 0

        # Each datasource should have XML element preserved
        for ds in workbook.datasources:
            assert ds.xml_element is not None
            assert ds.name is not None

        print(f"\n✓ Workbook structure validated")
        if workbook.dashboards:
            print(f"  First dashboard: {workbook.dashboards[0].name}")
        if workbook.worksheets:
            print(f"  First worksheet: {workbook.worksheets[0].name}")


if __name__ == "__main__":
    # Run tests with output
    pytest.main([__file__, "-v", "-s"])
