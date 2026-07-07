"""
Tableau Workbook Data Models

Represents the structure of a Tableau workbook with dashboards, worksheets, and formatting.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from lxml import etree


@dataclass
class Format:
    """Represents formatting/styling properties"""
    background_color: Optional[str] = None
    font_family: Optional[str] = None
    font_size: Optional[int] = None
    font_weight: Optional[str] = None
    font_color: Optional[str] = None
    border_color: Optional[str] = None
    border_width: Optional[int] = None
    padding: Optional[int] = None

    # XML element for direct manipulation
    xml_element: Optional[etree._Element] = None


@dataclass
class Worksheet:
    """Represents a Tableau worksheet"""
    name: str
    title: Optional[str] = None
    format: Format = field(default_factory=Format)

    # Raw XML for direct manipulation
    xml_element: Optional[etree._Element] = None


@dataclass
class Dashboard:
    """Represents a Tableau dashboard"""
    name: str
    title: Optional[str] = None
    worksheets: List[Worksheet] = field(default_factory=list)
    format: Format = field(default_factory=Format)

    # Raw XML for direct manipulation
    xml_element: Optional[etree._Element] = None


@dataclass
class Datasource:
    """Represents a Tableau datasource (preserved, not modified)"""
    name: str
    caption: Optional[str] = None

    # Raw XML - never modified by styling engine
    xml_element: Optional[etree._Element] = None


@dataclass
class Workbook:
    """Represents a complete Tableau workbook"""
    file_path: str
    file_type: str  # 'twb' or 'twbx'
    version: str

    dashboards: List[Dashboard] = field(default_factory=list)
    worksheets: List[Worksheet] = field(default_factory=list)
    datasources: List[Datasource] = field(default_factory=list)

    preferences: Dict[str, Any] = field(default_factory=dict)

    # Complete XML tree for manipulation
    xml_tree: Optional[etree._ElementTree] = None
    xml_root: Optional[etree._Element] = None

    # Original zip contents for .twbx files (images, data extracts)
    zip_contents: Optional[Dict[str, bytes]] = None

    def get_dashboard(self, name: str) -> Optional[Dashboard]:
        """Find dashboard by name"""
        for dashboard in self.dashboards:
            if dashboard.name == name:
                return dashboard
        return None

    def get_worksheet(self, name: str) -> Optional[Worksheet]:
        """Find worksheet by name"""
        for worksheet in self.worksheets:
            if worksheet.name == name:
                return worksheet
        return None
