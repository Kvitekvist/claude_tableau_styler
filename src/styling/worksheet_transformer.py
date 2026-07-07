"""
Worksheet Transformer

Optimizes individual worksheet elements: tables, charts, KPI cards.
Applies professional formatting to improve readability and visual appeal.
"""

from lxml import etree
from parser.workbook import Workbook
from config.style_config import StyleTemplate


class WorksheetTransformer:
    """Transforms worksheet-level visualizations for professional polish"""

    def apply(self, workbook: Workbook, template: StyleTemplate) -> None:
        """
        Apply worksheet optimizations

        Args:
            workbook: Workbook to modify
            template: Style template with configuration
        """
        self._optimize_tables(workbook, template)
        self._optimize_charts(workbook, template)
        self._optimize_kpi_cards(workbook, template)
        self._optimize_legends(workbook, template)

    def _optimize_tables(self, workbook: Workbook, template: StyleTemplate) -> None:
        """
        Optimize table formatting for better readability

        - Alternating row colors
        - Proper cell spacing
        - Clean borders
        - Header styling
        """
        if workbook.xml_root is None:
            return

        # Find all worksheets with tables
        for worksheet_elem in workbook.xml_root.findall('.//worksheet'):
            style = worksheet_elem.find('.//style')
            if style is None:
                style = etree.SubElement(worksheet_elem, 'style')

            # Find or create table style-rule
            table_rule = self._find_or_create_style_rule(style, 'table')

            # Alternating row colors (subtle)
            self._set_format_value(table_rule, 'band-color', '#F8F9FA', scope='rows')
            self._set_format_value(table_rule, 'band-size', '1', scope='rows')

            # Table background
            self._set_format_value(table_rule, 'background-color', '#FFFFFF')

            # Cell padding and spacing
            pane_spec = worksheet_elem.find('.//pane-specification')
            if pane_spec is not None:
                # Find format elements in pane-specification
                for fmt in pane_spec.findall('.//format'):
                    attr = fmt.get('attr')
                    # Increase cell height for better readability
                    if attr == 'cell-h':
                        current_height = int(fmt.get('value', '20'))
                        if current_height < 25:
                            fmt.set('value', '25')  # Minimum row height

            # Header row styling
            header_rule = self._find_or_create_style_rule(style, 'header')
            self._set_format_value(header_rule, 'background-color', '#F2F2F2')
            self._set_format_value(header_rule, 'font-weight', 'bold')
            self._set_format_value(header_rule, 'text-align', 'left')

            # Cell text alignment
            cell_rule = self._find_or_create_style_rule(style, 'cell')
            # Keep center alignment if it exists, otherwise left-align text cells
            existing_align = self._get_format_value(cell_rule, 'text-align')
            if not existing_align:
                self._set_format_value(cell_rule, 'text-align', 'left')

    def _optimize_charts(self, workbook: Workbook, template: StyleTemplate) -> None:
        """
        Optimize chart formatting

        - Chart padding and spacing
        - Axis formatting
        """
        if workbook.xml_root is None:
            return

        for worksheet_elem in workbook.xml_root.findall('.//worksheet'):
            style = worksheet_elem.find('.//style')
            if style is None:
                continue

            # Chart padding (increase whitespace around charts)
            pane_rule = self._find_or_create_style_rule(style, 'pane')
            self._set_format_value(pane_rule, 'padding', '12')

    def _optimize_kpi_cards(self, workbook: Workbook, template: StyleTemplate) -> None:
        """
        Optimize KPI card formatting

        - Large, prominent numbers
        - Clear visual hierarchy
        - Centered alignment
        - Proper spacing
        """
        if workbook.xml_root is None:
            return

        # KPI cards are typically single-number worksheets with center alignment
        for worksheet_elem in workbook.xml_root.findall('.//worksheet'):
            # Check if this is a KPI card (has center-aligned cells, no axes)
            style = worksheet_elem.find('.//style')
            if style is None:
                continue

            # Look for cell center alignment (KPI indicator)
            cell_rule = None
            for rule in style.findall('.//style-rule[@element="cell"]'):
                for fmt in rule.findall('.//format[@attr="text-align"]'):
                    if fmt.get('value') == 'center':
                        cell_rule = rule
                        break

            if cell_rule is not None:
                # This is likely a KPI card - optimize it
                # Increase font size for the number
                self._set_format_value(cell_rule, 'font-size', '28')
                self._set_format_value(cell_rule, 'font-weight', 'bold')
                self._set_format_value(cell_rule, 'font-family', 'Arial')
                self._set_format_value(cell_rule, 'color', template.colors.brand.get('primary_burgundy', '#7E2D25'))

                # Worksheet level styling for KPI
                worksheet_rule = self._find_or_create_style_rule(style, 'worksheet')
                self._set_format_value(worksheet_rule, 'padding', '16')

    def _optimize_legends(self, workbook: Workbook, template: StyleTemplate) -> None:
        """
        Optimize legend formatting - limited by Tableau's supported elements

        Note: Tableau doesn't support legend-title or legend-label as style-rule elements.
        Legend styling must be done through other means or manually.
        """
        # Skip - legend styling not supported via XML manipulation
        pass

    def _find_or_create_style_rule(self, style: etree._Element, element: str) -> etree._Element:
        """
        Find or create a style-rule for the given element

        Args:
            style: Style XML element
            element: Element name (e.g., 'table', 'cell', 'mark')

        Returns:
            style-rule element
        """
        # Look for existing rule
        for rule in style.findall('style-rule'):
            if rule.get('element') == element:
                return rule

        # Create new rule
        rule = etree.SubElement(style, 'style-rule')
        rule.set('element', element)
        return rule

    def _set_format_value(self, style_rule: etree._Element, attr: str, value: str, scope: str = None) -> None:
        """
        Set a format attribute value in a style-rule

        Args:
            style_rule: style-rule XML element
            attr: Format attribute name
            value: Format attribute value
            scope: Optional scope (e.g., 'rows', 'cols')
        """
        # Find existing format element
        format_elem = None
        for fmt in style_rule.findall('format'):
            if fmt.get('attr') == attr:
                # Check scope matches if specified
                if scope is None or fmt.get('scope') == scope:
                    format_elem = fmt
                    break

        if format_elem is None:
            format_elem = etree.SubElement(style_rule, 'format')
            format_elem.set('attr', attr)
            if scope:
                format_elem.set('scope', scope)

        format_elem.set('value', str(value))

    def _get_format_value(self, style_rule: etree._Element, attr: str) -> str:
        """
        Get a format attribute value from a style-rule

        Args:
            style_rule: style-rule XML element
            attr: Format attribute name

        Returns:
            Format value or empty string if not found
        """
        for fmt in style_rule.findall('format'):
            if fmt.get('attr') == attr:
                return fmt.get('value', '')
        return ''
