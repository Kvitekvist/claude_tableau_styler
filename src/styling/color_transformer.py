"""
Color Transformer

Applies color palette transformations to Tableau workbook.
"""

from lxml import etree
from parser.workbook import Workbook
from config.style_config import StyleTemplate


class ColorTransformer:
    """Transforms colors in Tableau workbook"""

    def apply(self, workbook: Workbook, template: StyleTemplate) -> None:
        """
        Apply color transformations to workbook

        Args:
            workbook: Workbook to modify
            template: Style template with color configuration
        """
        # Apply dashboard background colors
        self._apply_dashboard_colors(workbook, template)

        # Apply worksheet colors
        self._apply_worksheet_colors(workbook, template)

        # Apply color palettes (categorical, sequential, diverging)
        self._apply_color_palettes(workbook, template)

        # Apply specific element colors (gridlines, borders, etc.)
        self._apply_element_colors(workbook, template)

    def _apply_dashboard_colors(self, workbook: Workbook, template: StyleTemplate) -> None:
        """Apply colors to dashboards"""
        for dashboard in workbook.dashboards:
            if dashboard.xml_element is None:
                continue

            # Set dashboard background color
            bg_color = template.layout.dashboard.background_color
            self._set_background_color(dashboard.xml_element, bg_color)

    def _apply_worksheet_colors(self, workbook: Workbook, template: StyleTemplate) -> None:
        """Apply colors to worksheets"""
        for worksheet in workbook.worksheets:
            if worksheet.xml_element is None:
                continue

            # Set worksheet background color
            bg_color = template.layout.sheets.background_color
            self._set_background_color(worksheet.xml_element, bg_color)

    def _apply_color_palettes(self, workbook: Workbook, template: StyleTemplate) -> None:
        """
        Apply color palettes to workbook

        This modifies the workbook-level color palette definitions
        that charts reference.
        """
        if workbook.xml_root is None:
            return

        # Find or create preferences/color-palette section
        prefs = workbook.xml_root.find('preferences')
        if prefs is None:
            prefs = etree.SubElement(workbook.xml_root, 'preferences')

        # Apply categorical palette
        if template.colors.categorical:
            self._set_categorical_palette(prefs, template.colors.categorical)

    def _apply_element_colors(self, workbook: Workbook, template: StyleTemplate) -> None:
        """Apply colors to specific elements (gridlines, borders, etc.)"""
        # This is a simplified implementation
        # Full implementation would traverse all worksheet elements
        pass

    def _set_background_color(self, element: etree._Element, color: str) -> None:
        """
        Set background color on an element

        Args:
            element: XML element to modify
            color: Hex color code (#RRGGBB)
        """
        # Find or create style element
        style = element.find('style')
        if style is None:
            style = etree.SubElement(element, 'style')

        # Find or create format element for background
        format_elem = None
        for fmt in style.findall('.//format'):
            if fmt.get('attr') == 'background-color':
                format_elem = fmt
                break

        if format_elem is None:
            format_elem = etree.SubElement(style, 'format')
            format_elem.set('attr', 'background-color')

        # Set the color value
        format_elem.set('value', color)

    def _set_categorical_palette(self, prefs: etree._Element, colors: list) -> None:
        """
        Set categorical color palette

        Args:
            prefs: Preferences XML element
            colors: List of hex color codes
        """
        # Find or create color-palette
        palette = prefs.find('color-palette')
        if palette is None:
            palette = etree.SubElement(prefs, 'color-palette')
            palette.set('name', 'custom-palette')
            palette.set('type', 'regular')

        # Clear existing colors
        for color_elem in palette.findall('color'):
            palette.remove(color_elem)

        # Add new colors
        for color in colors:
            color_elem = etree.SubElement(palette, 'color')
            color_elem.text = color

    def _hex_to_tableau_color(self, hex_color: str) -> str:
        """
        Convert hex color to Tableau's color format if needed

        Args:
            hex_color: Color in #RRGGBB format

        Returns:
            Tableau-compatible color string
        """
        # Tableau typically uses #RRGGBB format directly
        return hex_color
