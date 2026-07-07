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
        # Apply comprehensive font replacement to ALL formatted text
        self._apply_to_formatted_text(workbook, template)

    def _apply_to_formatted_text(self, workbook: Workbook, template: StyleTemplate) -> None:
        """
        Apply typography to ALL formatted text elements comprehensively

        This replaces all Times New Roman fonts, standardizes sizes by context,
        and ensures consistent color hierarchy throughout the dashboard.
        """
        if workbook.xml_root is None:
            return

        # Find ALL formatted-text elements globally
        for text_elem in workbook.xml_root.findall('.//formatted-text'):
            for run in text_elem.findall('.//run'):
                # Get current font attributes
                font_name = run.get('fontname', '')
                font_size_str = run.get('fontsize', '11')

                # Parse font size safely
                try:
                    font_size = int(font_size_str)
                except (ValueError, TypeError):
                    font_size = 11

                # Determine context based on font size and apply appropriate styling
                # Dashboard titles (20pt+)
                if font_size >= 20:
                    run.set('fontname', template.typography.title.font_family)
                    run.set('fontsize', str(template.typography.title.font_size))
                    if template.typography.title.color:
                        run.set('fontcolor', template.typography.title.color)
                    if template.typography.title.font_weight == 'bold':
                        run.set('bold', 'true')

                # Sheet titles / section headers (12-19pt)
                elif 12 <= font_size < 20:
                    run.set('fontname', template.typography.sheet_title.font_family)
                    run.set('fontsize', str(template.typography.sheet_title.font_size))
                    if template.typography.sheet_title.color:
                        run.set('fontcolor', template.typography.sheet_title.color)
                    if template.typography.sheet_title.font_weight == 'bold':
                        run.set('bold', 'true')

                # Body text / labels (8-11pt)
                else:
                    run.set('fontname', template.typography.body.font_family)
                    # Keep existing size for body text to preserve layout
                    if template.typography.body.color:
                        run.set('fontcolor', template.typography.body.color)

                # CRITICAL: Replace Times New Roman regardless of size
                if 'Times New Roman' in font_name:
                    run.set('fontname', template.typography.body.font_family)

