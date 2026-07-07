"""
Tableau File Parser

Reads .twb (XML) and .twbx (ZIP containing XML) Tableau workbook files.
Extracts structure and formatting into Python objects for styling.
"""

import os
import zipfile
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Dict
from lxml import etree

from .workbook import Workbook, Dashboard, Worksheet, Datasource, Format


class TableauParserError(Exception):
    """Base exception for parser errors"""
    pass


class InvalidTableauFileError(TableauParserError):
    """File is not a valid Tableau workbook"""
    pass


class TableauParser:
    """Parser for Tableau workbook files"""

    def __init__(self):
        self.temp_dir: Optional[str] = None

    def parse(self, file_path: str) -> Workbook:
        """
        Parse a Tableau workbook file (.twb or .twbx)

        Args:
            file_path: Path to .twb or .twbx file

        Returns:
            Workbook object with parsed structure

        Raises:
            InvalidTableauFileError: If file is not a valid Tableau workbook
            FileNotFoundError: If file doesn't exist
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_ext = Path(file_path).suffix.lower()

        if file_ext == '.twbx':
            return self._parse_twbx(file_path)
        elif file_ext == '.twb':
            return self._parse_twb(file_path)
        else:
            raise InvalidTableauFileError(
                f"Invalid file type: {file_ext}. Expected .twb or .twbx"
            )

    def _parse_twbx(self, file_path: str) -> Workbook:
        """Parse a .twbx file (ZIP archive)"""
        try:
            # Create temp directory for extraction
            self.temp_dir = tempfile.mkdtemp(prefix='tableau_parser_')

            # Extract zip contents
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)

            # Find the .twb file inside
            twb_file = None
            zip_contents = {}

            for root, dirs, files in os.walk(self.temp_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.temp_dir)

                    if file.endswith('.twb'):
                        twb_file = full_path
                    else:
                        # Store other files (images, data extracts) for later
                        with open(full_path, 'rb') as f:
                            zip_contents[rel_path] = f.read()

            if not twb_file:
                raise InvalidTableauFileError("No .twb file found inside .twbx archive")

            # Parse the .twb XML file
            workbook = self._parse_twb(twb_file, file_type='twbx')
            workbook.file_path = file_path
            workbook.zip_contents = zip_contents

            return workbook

        except zipfile.BadZipFile:
            raise InvalidTableauFileError(f"Invalid ZIP archive: {file_path}")

        finally:
            # Clean up temp directory
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                self.temp_dir = None

    def _parse_twb(self, file_path: str, file_type: str = 'twb') -> Workbook:
        """Parse a .twb file (XML)"""
        try:
            # Parse XML
            tree = etree.parse(file_path)
            root = tree.getroot()

            # Verify it's a Tableau workbook
            if root.tag != 'workbook':
                raise InvalidTableauFileError(
                    f"Invalid XML root element: {root.tag}. Expected 'workbook'"
                )

            # Extract version
            version = root.get('version', 'unknown')

            # Create workbook object
            workbook = Workbook(
                file_path=file_path,
                file_type=file_type,
                version=version,
                xml_tree=tree,
                xml_root=root
            )

            # Parse preferences
            workbook.preferences = self._parse_preferences(root)

            # Parse datasources (preserve but don't modify)
            workbook.datasources = self._parse_datasources(root)

            # Parse worksheets
            workbook.worksheets = self._parse_worksheets(root)

            # Parse dashboards
            workbook.dashboards = self._parse_dashboards(root)

            return workbook

        except etree.XMLSyntaxError as e:
            raise InvalidTableauFileError(f"Invalid XML syntax: {e}")
        except Exception as e:
            raise TableauParserError(f"Failed to parse Tableau workbook: {e}")

    def _parse_preferences(self, root: etree._Element) -> Dict:
        """Extract preferences from workbook"""
        prefs = {}
        prefs_elem = root.find('preferences')
        if prefs_elem is not None:
            for key, value in prefs_elem.attrib.items():
                prefs[key] = value
        return prefs

    def _parse_datasources(self, root: etree._Element) -> list[Datasource]:
        """Extract datasources (read-only, never modified)"""
        datasources = []

        datasources_elem = root.find('datasources')
        if datasources_elem is not None:
            for ds_elem in datasources_elem.findall('datasource'):
                datasource = Datasource(
                    name=ds_elem.get('name', ''),
                    caption=ds_elem.get('caption'),
                    xml_element=ds_elem
                )
                datasources.append(datasource)

        return datasources

    def _parse_worksheets(self, root: etree._Element) -> list[Worksheet]:
        """Extract worksheets"""
        worksheets = []

        worksheets_elem = root.find('worksheets')
        if worksheets_elem is not None:
            for ws_elem in worksheets_elem.findall('worksheet'):
                worksheet = Worksheet(
                    name=ws_elem.get('name', ''),
                    title=self._extract_title(ws_elem),
                    format=self._extract_format(ws_elem),
                    xml_element=ws_elem
                )
                worksheets.append(worksheet)

        return worksheets

    def _parse_dashboards(self, root: etree._Element) -> list[Dashboard]:
        """Extract dashboards"""
        dashboards = []

        dashboards_elem = root.find('dashboards')
        if dashboards_elem is not None:
            for db_elem in dashboards_elem.findall('dashboard'):
                dashboard = Dashboard(
                    name=db_elem.get('name', ''),
                    title=self._extract_title(db_elem),
                    format=self._extract_format(db_elem),
                    xml_element=db_elem
                )
                dashboards.append(dashboard)

        return dashboards

    def _extract_title(self, element: etree._Element) -> Optional[str]:
        """Extract title from element if present"""
        # Tableau can store titles in various ways
        # This is a simplified extraction
        title_elem = element.find('.//formatted-text')
        if title_elem is not None:
            # Extract text content
            text = ''.join(title_elem.itertext())
            return text.strip() if text else None
        return None

    def _extract_format(self, element: etree._Element) -> Format:
        """Extract formatting properties from element"""
        fmt = Format()

        # Look for format/style child elements
        # Tableau stores formatting in various nested structures
        # This is a simplified extraction - full implementation would be more complex

        style_elem = element.find('.//style')
        if style_elem is not None:
            fmt.xml_element = style_elem

            # Extract color if present
            for child in style_elem:
                if 'color' in child.tag.lower():
                    fmt.background_color = child.get('value')
                elif 'font' in child.tag.lower():
                    fmt.font_family = child.get('family')
                    size = child.get('size')
                    if size:
                        try:
                            fmt.font_size = int(size)
                        except ValueError:
                            pass

        return fmt
