"""
Dashboard Transformer

Applies dashboard-specific styling: title zones, KPI cards,
filter styling, and modern card-based layouts.
"""

from lxml import etree
from parser.workbook import Workbook
from config.style_config import StyleTemplate


class DashboardTransformer:
    """Transforms dashboard-specific elements for modern professional look"""

    def apply(self, workbook: Workbook, template: StyleTemplate) -> None:
        """
        Apply dashboard transformations

        Args:
            workbook: Workbook to modify
            template: Style template with configuration
        """
        self._style_title_zones(workbook, template)
        self._style_kpi_cards(workbook, template)

    def _style_title_zones(self, workbook: Workbook, template: StyleTemplate) -> None:
        """
        Style title zones with clean modern look

        Removes harsh black backgrounds and borders,
        replaces with clean white professional styling.
        """
        if workbook.xml_root is None:
            return

        for zone in workbook.xml_root.findall('.//zone[@type-v2="title"]'):
            zone_style = zone.find('zone-style')
            if zone_style is None:
                zone_style = etree.SubElement(zone, 'zone-style')

            # Set background to white (not black)
            self._set_zone_format(zone_style, 'background-color', '#FFFFFF')

            # Remove harsh borders
            self._set_zone_format(zone_style, 'border-style', 'none')
            self._set_zone_format(zone_style, 'border-width', '0')

            # Increase padding for breathing room
            self._set_zone_format(zone_style, 'margin', '8')

    def _style_kpi_cards(self, workbook: Workbook, template: StyleTemplate) -> None:
        """
        Style KPI card zones for visual emphasis

        Applies light background to KPI zones for card-like appearance.
        """
        if workbook.xml_root is None:
            return

        # Find zones containing KPI worksheets (fixed-size zones)
        for zone in workbook.xml_root.findall('.//zone[@is-fixed="true"]'):
            zone_style = zone.find('zone-style')
            if zone_style is None:
                zone_style = etree.SubElement(zone, 'zone-style')

            # Check if it doesn't already have a background
            has_bg = any(f.get('attr') == 'background-color'
                       for f in zone_style.findall('format'))

            # Only add card background if no background exists
            if not has_bg:
                self._set_zone_format(zone_style, 'background-color',
                                    template.layout.containers.background_color)

    def _set_zone_format(self, zone_style: etree._Element, attr: str, value: str) -> None:
        """
        Helper to set or update format attribute in zone-style

        Args:
            zone_style: zone-style XML element
            attr: Format attribute name (e.g., 'background-color')
            value: Format attribute value
        """
        format_elem = None

        # Find existing format element with this attribute
        for fmt in zone_style.findall('format'):
            if fmt.get('attr') == attr:
                format_elem = fmt
                break

        # Create if doesn't exist
        if format_elem is None:
            format_elem = etree.SubElement(zone_style, 'format')
            format_elem.set('attr', attr)

        # Set the value
        format_elem.set('value', str(value))
