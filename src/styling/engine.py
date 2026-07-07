"""
Styling Engine

Applies style template transformations to Tableau workbook XML.
Modifies colors, typography, layout while preserving data connections and calculations.
"""

from typing import Optional
from lxml import etree
import copy

from parser.workbook import Workbook, Dashboard, Worksheet
from config.style_config import StyleTemplate

from styling.color_transformer import ColorTransformer
from styling.typography_transformer import TypographyTransformer
from styling.layout_transformer import LayoutTransformer
from styling.dashboard_transformer import DashboardTransformer
from styling.worksheet_transformer import WorksheetTransformer


class StylingEngineError(Exception):
    """Base exception for styling engine errors"""
    pass


class StylingEngine:
    """
    Core styling engine that applies templates to Tableau workbooks
    """

    def __init__(self):
        self.color_transformer = ColorTransformer()
        self.typography_transformer = TypographyTransformer()
        self.layout_transformer = LayoutTransformer()
        self.dashboard_transformer = DashboardTransformer()
        self.worksheet_transformer = WorksheetTransformer()

    def apply_template(self, workbook: Workbook, template: StyleTemplate) -> Workbook:
        """
        Apply a style template to a workbook

        Args:
            workbook: Parsed Tableau workbook
            template: Style template to apply

        Returns:
            Modified workbook with styling applied

        Note:
            Creates a deep copy to preserve original workbook
        """
        # Create a deep copy of the XML tree to avoid modifying original
        styled_workbook = copy.deepcopy(workbook)

        try:
            # Apply color transformations
            self.color_transformer.apply(styled_workbook, template)

            # Apply typography transformations
            self.typography_transformer.apply(styled_workbook, template)

            # Apply layout transformations
            self.layout_transformer.apply(styled_workbook, template)

            # Apply dashboard-specific styling (title zones, KPI cards)
            self.dashboard_transformer.apply(styled_workbook, template)

            # Apply worksheet optimizations (tables, charts, KPI cards)
            self.worksheet_transformer.apply(styled_workbook, template)

            # Validate the modified XML is still well-formed
            self._validate_workbook(styled_workbook)

            return styled_workbook

        except Exception as e:
            raise StylingEngineError(f"Failed to apply styling: {e}") from e

    def _validate_workbook(self, workbook: Workbook) -> None:
        """
        Validate that workbook XML is still well-formed after modifications

        Args:
            workbook: Styled workbook to validate

        Raises:
            StylingEngineError: If workbook is invalid
        """
        if workbook.xml_root is None:
            raise StylingEngineError("Workbook has no XML root element")

        # Verify root element is still 'workbook'
        if workbook.xml_root.tag != 'workbook':
            raise StylingEngineError(
                f"Invalid root element: {workbook.xml_root.tag}, expected 'workbook'"
            )

        # Verify datasources are still present (must be preserved)
        datasources_elem = workbook.xml_root.find('datasources')
        if datasources_elem is None and len(workbook.datasources) > 0:
            raise StylingEngineError("Datasources element was removed - this should never happen!")

        # Basic well-formedness check - can we serialize to string?
        try:
            etree.tostring(workbook.xml_root, encoding='unicode')
        except Exception as e:
            raise StylingEngineError(f"XML is not well-formed after styling: {e}") from e
