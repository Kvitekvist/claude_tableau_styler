"""
Dashboard Layout Builder

Creates professionally designed dashboard layouts following modern BI design guidelines.
Implements 12-column grid system, proper container hierarchy, and consistent spacing.
"""

from lxml import etree
from typing import List, Dict, Optional


class LayoutBuilder:
    """Builds dashboard layouts following design guidelines"""

    def __init__(self):
        # Spacing values from design guidelines
        self.OUTER_PADDING = 24
        self.SECTION_SPACING = 24
        self.KPI_SPACING = 16
        self.CARD_PADDING = 16
        self.CHART_PADDING = 16

        # Dimensions
        self.DASHBOARD_WIDTH = 1400
        self.DASHBOARD_HEIGHT = 1000

        # Grid system
        self.GRID_COLUMNS = 12
        self.COLUMN_WIDTH = (self.DASHBOARD_WIDTH - (2 * self.OUTER_PADDING)) // self.GRID_COLUMNS

        # Zone ID counter
        self.zone_id = 1

    def create_modern_dashboard(
        self,
        title: str,
        subtitle: str,
        kpi_worksheets: List[str],
        primary_chart: str,
        supporting_charts: List[str],
        table_worksheet: str,
        filters: List[str] = None
    ) -> etree._Element:
        """
        Create a modern executive dashboard with proper structure

        Args:
            title: Dashboard title
            subtitle: Dashboard subtitle
            kpi_worksheets: List of KPI worksheet names
            primary_chart: Main trend visualization worksheet
            supporting_charts: List of supporting chart worksheets
            table_worksheet: Detail table worksheet
            filters: Optional list of filter field names

        Returns:
            Dashboard XML element
        """
        dashboard = etree.Element('dashboard')
        dashboard.set('enable-sort-zone-taborder', 'true')
        dashboard.set('name', title.replace(' ', '_'))

        # Add title
        layout_options = etree.SubElement(dashboard, 'layout-options')
        self._add_title(layout_options, title, subtitle)

        # Main dashboard style
        style = etree.SubElement(dashboard, 'style')

        # Size configuration - fixed for consistency
        size = etree.SubElement(dashboard, 'size')
        size.set('maxheight', str(self.DASHBOARD_HEIGHT))
        size.set('maxwidth', str(self.DASHBOARD_WIDTH))
        size.set('minheight', str(self.DASHBOARD_HEIGHT))
        size.set('minwidth', str(self.DASHBOARD_WIDTH))
        size.set('sizing-mode', 'fixed')

        # Add datasources element (empty - worksheets have their own datasources)
        datasources = etree.SubElement(dashboard, 'datasources')

        # Create zones container
        zones = etree.SubElement(dashboard, 'zones')

        # Build structured layout
        self._build_layout(
            zones,
            kpi_worksheets,
            primary_chart,
            supporting_charts,
            table_worksheet,
            filters
        )

        # Add devicelayouts (required for responsive design)
        devicelayouts = etree.SubElement(dashboard, 'devicelayouts')

        # Add simple-id (required)
        simple_id = etree.SubElement(dashboard, 'simple-id')
        simple_id.set('uuid', '{' + 'A' * 8 + '-' + 'B' * 4 + '-' + 'C' * 4 + '-' + 'D' * 4 + '-' + 'E' * 12 + '}')

        return dashboard

    def _add_title(self, layout_options: etree._Element, title: str, subtitle: str) -> None:
        """Add formatted title to dashboard"""
        title_elem = etree.SubElement(layout_options, 'title')
        formatted_text = etree.SubElement(title_elem, 'formatted-text')

        # Main title
        title_run = etree.SubElement(formatted_text, 'run')
        title_run.set('bold', 'true')
        title_run.set('fontname', 'Arial')
        title_run.set('fontsize', '24')
        title_run.set('fontcolor', '#333333')
        title_run.text = title

        # Line break
        br_run = etree.SubElement(formatted_text, 'run')
        br_run.set('fontname', 'Arial')
        br_run.set('fontcolor', '#6B6B6B')
        br_run.text = '\n'

        # Subtitle
        subtitle_run = etree.SubElement(formatted_text, 'run')
        subtitle_run.set('fontname', 'Arial')
        subtitle_run.set('fontsize', '12')
        subtitle_run.set('fontcolor', '#6B6B6B')
        subtitle_run.text = subtitle

    def _build_layout(
        self,
        zones: etree._Element,
        kpi_worksheets: List[str],
        primary_chart: str,
        supporting_charts: List[str],
        table_worksheet: str,
        filters: Optional[List[str]]
    ) -> None:
        """
        Build the complete dashboard layout structure

        Layout hierarchy:
        - Root vertical container
          - Filter bar (if filters provided)
          - KPI cards row
          - Primary trend chart
          - Supporting charts row
          - Detail table
        """
        # Root container - fills entire dashboard with outer padding
        root_zone = etree.SubElement(zones, 'zone')
        root_zone.set('h', str(self.DASHBOARD_HEIGHT - (2 * self.OUTER_PADDING)))
        root_zone.set('w', str(self.DASHBOARD_WIDTH - (2 * self.OUTER_PADDING)))
        root_zone.set('x', str(self.OUTER_PADDING))
        root_zone.set('y', str(self.OUTER_PADDING))
        root_zone.set('type-v2', 'layout-flow')
        root_zone.set('param', 'vert')
        root_zone.set('id', '1')

        current_y = 0

        # Filter bar (if provided)
        if filters:
            filter_height = 60
            self._add_filter_bar(root_zone, filters, filter_height)
            current_y += filter_height + self.SECTION_SPACING

        # KPI cards row
        kpi_height = 120
        self._add_kpi_row(root_zone, kpi_worksheets, kpi_height)
        current_y += kpi_height + self.SECTION_SPACING

        # Primary trend chart (largest visualization)
        trend_height = 300
        self._add_primary_chart(root_zone, primary_chart, trend_height)
        current_y += trend_height + self.SECTION_SPACING

        # Supporting charts row (side by side)
        supporting_height = 220
        if supporting_charts:
            self._add_supporting_charts(root_zone, supporting_charts, supporting_height)
            current_y += supporting_height + self.SECTION_SPACING

        # Detail table (compact, scrollable)
        table_height = 200
        self._add_detail_table(root_zone, table_worksheet, table_height)

    def _add_kpi_row(self, parent: etree._Element, kpi_worksheets: List[str], height: int) -> None:
        """Add horizontal row of equal-width KPI cards"""
        kpi_container = etree.SubElement(parent, 'zone')
        kpi_container.set('id', str(self.zone_id))
        self.zone_id += 1
        kpi_container.set('type-v2', 'layout-flow')
        kpi_container.set('param', 'horz')
        kpi_container.set('h', str(height))
        kpi_container.set('w', str(self.DASHBOARD_WIDTH - (2 * self.OUTER_PADDING)))
        kpi_container.set('x', '0')
        kpi_container.set('y', '0')

        num_kpis = len(kpi_worksheets)
        available_width = self.DASHBOARD_WIDTH - (2 * self.OUTER_PADDING)
        total_spacing = self.KPI_SPACING * (num_kpis - 1)
        kpi_width = (available_width - total_spacing) // num_kpis

        x_pos = 0
        for i, worksheet_name in enumerate(kpi_worksheets):
            kpi_zone = etree.SubElement(kpi_container, 'zone')
            kpi_zone.set('id', str(self.zone_id))
            self.zone_id += 1
            kpi_zone.set('name', worksheet_name)
            kpi_zone.set('w', str(kpi_width))
            kpi_zone.set('h', str(height))
            kpi_zone.set('x', str(x_pos))
            kpi_zone.set('y', '0')
            kpi_zone.set('type-v2', 'layout-basic')

            # Add card styling
            zone_style = etree.SubElement(kpi_zone, 'zone-style')
            self._add_format(zone_style, 'background-color', '#FFFFFF')
            self._add_format(zone_style, 'border-color', '#E0E0E0')
            self._add_format(zone_style, 'border-width', '1')
            self._add_format(zone_style, 'border-style', 'solid')
            self._add_format(zone_style, 'margin', str(self.CARD_PADDING))

            x_pos += kpi_width + self.KPI_SPACING

    def _add_primary_chart(self, parent: etree._Element, worksheet_name: str, height: int) -> None:
        """Add primary trend visualization (full width)"""
        chart_zone = etree.SubElement(parent, 'zone')
        chart_zone.set('id', str(self.zone_id))
        self.zone_id += 1
        chart_zone.set('name', worksheet_name)
        chart_zone.set('h', str(height))
        chart_zone.set('w', str(self.DASHBOARD_WIDTH - (2 * self.OUTER_PADDING)))
        chart_zone.set('x', '0')
        chart_zone.set('y', '0')
        chart_zone.set('type-v2', 'layout-basic')

        # Add subtle card background
        zone_style = etree.SubElement(chart_zone, 'zone-style')
        self._add_format(zone_style, 'background-color', '#FFFFFF')
        self._add_format(zone_style, 'border-color', '#E0E0E0')
        self._add_format(zone_style, 'border-width', '1')
        self._add_format(zone_style, 'border-style', 'solid')
        self._add_format(zone_style, 'margin', str(self.CHART_PADDING))

    def _add_supporting_charts(self, parent: etree._Element, worksheets: List[str], height: int) -> None:
        """Add horizontal row of supporting charts (equal width)"""
        chart_container = etree.SubElement(parent, 'zone')
        chart_container.set('id', str(self.zone_id))
        self.zone_id += 1
        chart_container.set('type-v2', 'layout-flow')
        chart_container.set('param', 'horz')
        chart_container.set('h', str(height))
        chart_container.set('w', str(self.DASHBOARD_WIDTH - (2 * self.OUTER_PADDING)))
        chart_container.set('x', '0')
        chart_container.set('y', '0')

        num_charts = len(worksheets)
        available_width = self.DASHBOARD_WIDTH - (2 * self.OUTER_PADDING)
        total_spacing = self.SECTION_SPACING * (num_charts - 1)
        chart_width = (available_width - total_spacing) // num_charts

        x_pos = 0
        for worksheet_name in worksheets:
            chart_zone = etree.SubElement(chart_container, 'zone')
            chart_zone.set('id', str(self.zone_id))
            self.zone_id += 1
            chart_zone.set('name', worksheet_name)
            chart_zone.set('w', str(chart_width))
            chart_zone.set('h', str(height))
            chart_zone.set('x', str(x_pos))
            chart_zone.set('y', '0')
            chart_zone.set('type-v2', 'layout-basic')

            zone_style = etree.SubElement(chart_zone, 'zone-style')
            self._add_format(zone_style, 'background-color', '#FFFFFF')
            self._add_format(zone_style, 'border-color', '#E0E0E0')
            self._add_format(zone_style, 'border-width', '1')
            self._add_format(zone_style, 'border-style', 'solid')
            self._add_format(zone_style, 'margin', str(self.CHART_PADDING))

            x_pos += chart_width + self.SECTION_SPACING

    def _add_detail_table(self, parent: etree._Element, worksheet_name: str, height: int) -> None:
        """Add detail table (full width, scrollable)"""
        table_zone = etree.SubElement(parent, 'zone')
        table_zone.set('id', str(self.zone_id))
        self.zone_id += 1
        table_zone.set('name', worksheet_name)
        table_zone.set('h', str(height))
        table_zone.set('w', str(self.DASHBOARD_WIDTH - (2 * self.OUTER_PADDING)))
        table_zone.set('x', '0')
        table_zone.set('y', '0')
        table_zone.set('type-v2', 'layout-basic')

        zone_style = etree.SubElement(table_zone, 'zone-style')
        self._add_format(zone_style, 'background-color', '#FFFFFF')
        self._add_format(zone_style, 'border-color', '#E0E0E0')
        self._add_format(zone_style, 'border-width', '1')
        self._add_format(zone_style, 'border-style', 'solid')

    def _add_filter_bar(self, parent: etree._Element, filters: List[str], height: int) -> None:
        """Add horizontal filter bar"""
        # Placeholder - filters need special handling in Tableau
        pass

    def _add_format(self, zone_style: etree._Element, attr: str, value: str) -> None:
        """Helper to add format element to zone-style"""
        format_elem = etree.SubElement(zone_style, 'format')
        format_elem.set('attr', attr)
        format_elem.set('value', value)
