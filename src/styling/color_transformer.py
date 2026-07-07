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
        # Apply colors to chart marks (bars, lines, shapes)
        self._apply_chart_mark_colors(workbook, template)

        # Apply grid line colors
        self._apply_gridline_colors(workbook, template)

        # Apply axis colors
        self._apply_axis_colors(workbook, template)

    def _apply_chart_mark_colors(self, workbook: Workbook, template: StyleTemplate) -> None:
        """
        Apply template colors to chart marks (bars, lines, shapes)

        Modifies <style-rule element='mark'> with <encoding attr='color'>
        """
        if workbook.xml_root is None:
            return

        # Get categorical palette from template
        palette = template.colors.categorical
        if not palette:
            return

        # Find all worksheets in XML
        for worksheet_elem in workbook.xml_root.findall('.//worksheet'):
            # Find all style-rule elements for marks
            for style_rule in worksheet_elem.findall('.//style-rule[@element="mark"]'):
                # Find color encodings
                for encoding in style_rule.findall('.//encoding[@attr="color"]'):
                    # Update color maps with template palette
                    maps = encoding.findall('map')
                    for i, map_elem in enumerate(maps):
                        # Cycle through template palette
                        new_color = palette[i % len(palette)]
                        map_elem.set('to', new_color)

    def _apply_gridline_colors(self, workbook: Workbook, template: StyleTemplate) -> None:
        """Apply gridline colors from template"""
        if workbook.xml_root is None:
            return

        gridline_color = template.chart_elements.gridlines.color

        # Find all worksheets
        for worksheet_elem in workbook.xml_root.findall('.//worksheet'):
            # Find or create style section
            style = worksheet_elem.find('.//style')
            if style is None:
                continue

            # Find or create gridline style-rule
            grid_rule = None
            for rule in style.findall('style-rule'):
                if rule.get('element') == 'gridline':
                    grid_rule = rule
                    break

            if grid_rule is None:
                grid_rule = etree.SubElement(style, 'style-rule')
                grid_rule.set('element', 'gridline')

            # Set gridline color only (opacity not supported by Tableau)
            self._set_format_value(grid_rule, 'stroke-color', gridline_color)

    def _apply_axis_colors(self, workbook: Workbook, template: StyleTemplate) -> None:
        """Apply axis colors from template"""
        if workbook.xml_root is None:
            return

        axis_color = template.chart_elements.axes.line_color

        # Find all worksheets
        for worksheet_elem in workbook.xml_root.findall('.//worksheet'):
            # Find or create style section
            style = worksheet_elem.find('.//style')
            if style is None:
                continue

            # Find or create axis style-rule
            axis_rule = None
            for rule in style.findall('style-rule'):
                if rule.get('element') == 'axis':
                    axis_rule = rule
                    break

            if axis_rule is None:
                axis_rule = etree.SubElement(style, 'style-rule')
                axis_rule.set('element', 'axis')

            # Set axis color
            self._set_format_value(axis_rule, 'stroke-color', axis_color)

    def _set_format_value(self, parent: etree._Element, attr: str, value: str) -> None:
        """Set a format attribute value in a style-rule"""
        # Find existing format element
        format_elem = None
        for fmt in parent.findall('format'):
            if fmt.get('attr') == attr:
                format_elem = fmt
                break

        if format_elem is None:
            format_elem = etree.SubElement(parent, 'format')
            format_elem.set('attr', attr)

        format_elem.set('value', value)

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
