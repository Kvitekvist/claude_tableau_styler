"""
Typography Transformer

Applies font and text styling to Tableau workbook.
"""

from lxml import etree
from parser.workbook import Workbook
from config.style_config import StyleTemplate, TypographyStyle


class TypographyTransformer:
    """Transforms typography in Tableau workbook"""

    def apply(self, workbook: Workbook, template: StyleTemplate) -> None:
        """
        Apply typography transformations to workbook

        Args:
            workbook: Workbook to modify
            template: Style template with typography configuration
        """
        # Apply dashboard title fonts
        self._apply_dashboard_titles(workbook, template)

        # Apply worksheet title fonts
        self._apply_worksheet_titles(workbook, template)

        # Apply body text fonts
        self._apply_body_text(workbook, template)

    def _apply_dashboard_titles(self, workbook: Workbook, template: StyleTemplate) -> None:
        """Apply typography to dashboard titles"""
        title_style = template.typography.title

        for dashboard in workbook.dashboards:
            if dashboard.xml_element is None:
                continue

            # Find title elements
            for title_elem in dashboard.xml_element.findall('.//formatted-text'):
                self._apply_typography_style(title_elem, title_style)

    def _apply_worksheet_titles(self, workbook: Workbook, template: StyleTemplate) -> None:
        """Apply typography to worksheet titles"""
        title_style = template.typography.sheet_title

        for worksheet in workbook.worksheets:
            if worksheet.xml_element is None:
                continue

            # Find title elements
            for title_elem in worksheet.xml_element.findall('.//formatted-text'):
                self._apply_typography_style(title_elem, title_style)

    def _apply_body_text(self, workbook: Workbook, template: StyleTemplate) -> None:
        """Apply typography to body text elements"""
        body_style = template.typography.body

        # This would apply to labels, annotations, tooltips, etc.
        # Simplified implementation
        pass

    def _apply_typography_style(self, element: etree._Element, style: TypographyStyle) -> None:
        """
        Apply typography style to a formatted text element

        Args:
            element: Formatted text XML element
            style: Typography style to apply
        """
        # Find or create run element (Tableau's text formatting structure)
        run = element.find('.//run')
        if run is None:
            # Create basic structure if missing
            run = etree.SubElement(element, 'run')

        # Set font family
        run.set('fontname', style.font_family)

        # Set font size
        run.set('fontsize', str(style.font_size))

        # Set font weight (bold/normal)
        if style.font_weight == 'bold':
            run.set('bold', 'true')
        else:
            run.set('bold', 'false')

        # Set font color
        run.set('foreground', style.color)
