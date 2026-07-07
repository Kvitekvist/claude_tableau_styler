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
        self._optimize_text_marks(workbook, template)
        self._optimize_legends(workbook, template)

    def _optimize_tables(self, workbook: Workbook, template: StyleTemplate) -> None:
        """
        Optimize table formatting for better readability

        - Alternating row colors (more visible)
        - Larger fonts
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

            # Alternating row colors - make MORE visible
            self._set_format_value(table_rule, 'band-color', '#F0F0F0', scope='rows')  # Darker gray
            self._set_format_value(table_rule, 'band-size', '1', scope='rows')

            # Table background
            self._set_format_value(table_rule, 'background-color', '#FFFFFF')

            # Increase font size for better readability
            self._set_format_value(table_rule, 'font-size', '11')
            self._set_format_value(table_rule, 'font-family', 'Arial')

            # Cell padding and spacing
            pane_spec = worksheet_elem.find('.//pane-specification')
            if pane_spec is not None:
                # Find format elements in pane-specification
                for fmt in pane_spec.findall('.//format'):
                    attr = fmt.get('attr')
                    # Increase cell height for better readability
                    if attr == 'cell-h':
                        current_height = int(fmt.get('value', '20'))
                        if current_height < 28:
                            fmt.set('value', '28')  # Taller rows for breathing room

            # Header row styling
            header_rule = self._find_or_create_style_rule(style, 'header')
            self._set_format_value(header_rule, 'background-color', '#E8E8E8')  # Slightly darker
            self._set_format_value(header_rule, 'font-weight', 'bold')
            self._set_format_value(header_rule, 'font-size', '12')
            self._set_format_value(header_rule, 'text-align', 'left')
            self._set_format_value(header_rule, 'color', '#333333')  # Dark text

            # Cell text styling
            cell_rule = self._find_or_create_style_rule(style, 'cell')
            # Keep center alignment if it exists, otherwise left-align text cells
            existing_align = self._get_format_value(cell_rule, 'text-align')
            if not existing_align or existing_align != 'center':
                self._set_format_value(cell_rule, 'text-align', 'left')

            # Make sure cell text is readable
            if not self._get_format_value(cell_rule, 'color'):
                self._set_format_value(cell_rule, 'color', '#333333')

    def _optimize_charts(self, workbook: Workbook, template: StyleTemplate) -> None:
        """
        Optimize chart formatting

        - Chart padding and spacing
        - Axis formatting
        - Label text color for better contrast
        """
        if workbook.xml_root is None:
            return

        for worksheet_elem in workbook.xml_root.findall('.//worksheet'):
            style = worksheet_elem.find('.//style')
            if style is None:
                continue

            # Chart padding (increase whitespace around charts)
            pane_rule = self._find_or_create_style_rule(style, 'pane')
            self._set_format_value(pane_rule, 'padding', '16')  # More padding

            # Fix mark labels (percentage labels on bars) - make them dark for readability
            # Find all format elements with mark-labels-cull-min-size and nearby text formatting
            for fmt in worksheet_elem.findall('.//format'):
                attr = fmt.get('attr')
                # Change white label text to dark for better contrast on burgundy bars
                if attr == 'color' and fmt.get('value') in ['#ffffff', '#FFFFFF']:
                    # Check if this is in a mark-related context
                    parent = fmt.getparent()
                    if parent is not None and parent.tag == 'style-rule':
                        if parent.get('element') == 'mark':
                            fmt.set('value', '#FFFFFF')  # Keep white for now
                        else:
                            fmt.set('value', '#333333')  # Dark text elsewhere

    def _optimize_kpi_cards(self, workbook: Workbook, template: StyleTemplate) -> None:
        """
        Optimize KPI card formatting

        - Large, prominent numbers
        - Clear visual hierarchy
        - Centered alignment
        - Proper spacing
        - Ensure visibility with proper background
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
                # LARGE font size for the number
                self._set_format_value(cell_rule, 'font-size', '36')  # Even larger!
                self._set_format_value(cell_rule, 'font-weight', 'bold')
                self._set_format_value(cell_rule, 'font-family', 'Arial')

                # Use dark burgundy for better visibility
                self._set_format_value(cell_rule, 'color', '#7E2D25')

                # Ensure white background so number is visible
                self._set_format_value(cell_rule, 'background-color', '#FFFFFF')

                # Worksheet level styling for KPI
                worksheet_rule = self._find_or_create_style_rule(style, 'worksheet')
                self._set_format_value(worksheet_rule, 'padding', '20')  # More padding
                self._set_format_value(worksheet_rule, 'background-color', '#FFFFFF')

    def _optimize_text_marks(self, workbook: Workbook, template: StyleTemplate) -> None:
        """
        Optimize text marks (labels on bars, annotations)

        Make text marks more readable by ensuring proper contrast.
        """
        if workbook.xml_root is None:
            return

        # Find all pane-specification elements which contain mark formatting
        for pane_spec in workbook.xml_root.findall('.//pane-specification'):
            # Look for text marks and adjust their color for readability
            for encoding in pane_spec.findall('.//encoding[@attr="text"]'):
                # Find format elements related to text color
                for fmt in encoding.findall('.//format'):
                    if fmt.get('attr') == 'color':
                        # Change white text to dark for better contrast
                        if fmt.get('value', '').upper() in ['#FFFFFF', '#FFFFFFFF']:
                            fmt.set('value', '#333333')

            # Also check style formats in pane
            for fmt in pane_spec.findall('.//format[@attr="font-weight"]'):
                # Make labels bold
                fmt.set('value', 'bold')

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
