"""
Layout Transformer

Applies layout and spacing transformations to Tableau workbook.
"""

from lxml import etree
from parser.workbook import Workbook
from config.style_config import StyleTemplate


class LayoutTransformer:
    """Transforms layout properties in Tableau workbook"""

    def apply(self, workbook: Workbook, template: StyleTemplate) -> None:
        """
        Apply layout transformations to workbook

        Args:
            workbook: Workbook to modify
            template: Style template with layout configuration
        """
        # Apply dashboard layout
        self._apply_dashboard_layout(workbook, template)

        # Apply container layout
        self._apply_container_layout(workbook, template)

        # Apply worksheet layout
        self._apply_worksheet_layout(workbook, template)

        # Apply zone-style background fixes (remove black backgrounds)
        self._apply_zone_style_backgrounds(workbook, template)

    def _apply_dashboard_layout(self, workbook: Workbook, template: StyleTemplate) -> None:
        """Apply layout properties to dashboards"""
        for dashboard in workbook.dashboards:
            if dashboard.xml_element is None:
                continue

            # Set padding on dashboard
            padding = template.layout.dashboard.padding
            self._set_padding(dashboard.xml_element, padding)

            # Apply padding to all zones in dashboard
            for zone in dashboard.xml_element.findall('.//zone'):
                self._set_padding(zone, padding)

    def _apply_container_layout(self, workbook: Workbook, template: StyleTemplate) -> None:
        """Apply layout properties to containers"""
        # Find all container elements in dashboards
        for dashboard in workbook.dashboards:
            if dashboard.xml_element is None:
                continue

            for container in dashboard.xml_element.findall('.//zone[@type="layout-basic"]'):
                # Set container background
                bg_color = template.layout.containers.background_color
                self._set_container_background(container, bg_color)

                # Set border
                border_color = template.layout.containers.border_color
                border_width = template.layout.containers.border_width
                self._set_border(container, border_color, border_width)

                # Set padding and spacing
                padding = template.layout.containers.padding
                self._set_padding(container, padding)

    def _apply_worksheet_layout(self, workbook: Workbook, template: StyleTemplate) -> None:
        """Apply layout properties to worksheets"""
        for worksheet in workbook.worksheets:
            if worksheet.xml_element is None:
                continue

            # Set worksheet background
            bg_color = template.layout.sheets.background_color
            self._set_worksheet_background(worksheet.xml_element, bg_color)

            # Set borders
            border_color = template.layout.sheets.border_color
            border_width = template.layout.sheets.border_width
            self._set_border(worksheet.xml_element, border_color, border_width)

    def _set_padding(self, element: etree._Element, padding: int) -> None:
        """Set padding and margin on zones and zone-styles"""
        # Tableau uses 'padding' attribute on zones
        if element.tag == 'zone':
            element.set('padding', str(padding))
            element.set('margin', str(padding // 2))  # Margin is half of padding

        # Also update zone-style if it exists
        zone_style = element.find('zone-style')
        if zone_style is not None:
            # Find or create margin format
            margin_fmt = None
            for fmt in zone_style.findall('format'):
                if fmt.get('attr') == 'margin':
                    margin_fmt = fmt
                    break

            if margin_fmt is None:
                margin_fmt = etree.SubElement(zone_style, 'format')
                margin_fmt.set('attr', 'margin')

            margin_fmt.set('value', str(padding // 2))

    def _set_container_background(self, element: etree._Element, color: str) -> None:
        """Set background color on container"""
        # Find or create style
        style = element.find('style')
        if style is None:
            style = etree.SubElement(element, 'style')

        # Set background format
        format_elem = etree.SubElement(style, 'format')
        format_elem.set('attr', 'background-color')
        format_elem.set('value', color)

    def _set_worksheet_background(self, element: etree._Element, color: str) -> None:
        """Set background color on worksheet"""
        # Similar to container, but for worksheet elements
        style = element.find('style')
        if style is None:
            style = etree.SubElement(element, 'style')

        format_elem = etree.SubElement(style, 'format')
        format_elem.set('attr', 'background-color')
        format_elem.set('value', color)

    def _set_border(self, element: etree._Element, color: str, width: int) -> None:
        """Set border on an element"""
        style = element.find('style')
        if style is None:
            style = etree.SubElement(element, 'style')

        # Border color
        border_color_elem = etree.SubElement(style, 'format')
        border_color_elem.set('attr', 'border-color')
        border_color_elem.set('value', color)

        # Border width
        border_width_elem = etree.SubElement(style, 'format')
        border_width_elem.set('attr', 'border-width')
        border_width_elem.set('value', str(width))

    def _apply_zone_style_backgrounds(self, workbook: Workbook, template: StyleTemplate) -> None:
        """
        Remove harsh black backgrounds from zone-style elements

        Replaces #000103, #000000, #000102 (black) backgrounds and borders
        with template colors for a modern, professional look.
        """
        if workbook.xml_root is None:
            return

        # Find all zone-style elements (used in title zones, floating elements)
        for zone_style in workbook.xml_root.findall('.//zone-style'):
            for format_elem in zone_style.findall('format'):
                attr = format_elem.get('attr')
                current = format_elem.get('value', '').lower()

                # Replace black backgrounds with white
                if attr == 'background-color':
                    if current in ['#000103', '#000000', '#000102', '#000001']:
                        format_elem.set('value', template.layout.dashboard.background_color)

                # Replace black borders with light gray
                elif attr == 'border-color':
                    if current in ['#000103', '#000000', '#000102', '#000001']:
                        format_elem.set('value', template.colors.neutrals.get('light_gray', '#F2F2F2'))
