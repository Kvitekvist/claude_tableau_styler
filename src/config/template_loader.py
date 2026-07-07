"""
YAML Template Configuration Loader

Loads and validates style template YAML files.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
import yaml

from .style_config import (
    StyleTemplate, Metadata, ColorPalette, Typography, TypographyStyle,
    Layout, DashboardLayout, ContainerLayout, SheetLayout,
    ChartElements, GridlineConfig, AxisConfig, ReferenceLineConfig,
    BorderConfig, ShadowConfig, NullValueConfig,
    ChartTypes, ChartTypeConfig, FilterConfig, RulesConfig
)


class TemplateLoaderError(Exception):
    """Base exception for template loader errors"""
    pass


class InvalidColorCodeError(TemplateLoaderError):
    """Invalid hex color code"""
    pass


class InvalidTemplateError(TemplateLoaderError):
    """Template file is invalid or malformed"""
    pass


class TemplateLoader:
    """Loader for YAML style templates"""

    # Hex color pattern: #RRGGBB
    COLOR_PATTERN = re.compile(r'^#[0-9A-Fa-f]{6}$')

    def __init__(self, templates_dir: str = "tableau/templates"):
        self.templates_dir = templates_dir

    def load(self, template_path: str) -> StyleTemplate:
        """
        Load a style template from YAML file

        Args:
            template_path: Path to YAML template file (relative or absolute)

        Returns:
            StyleTemplate object

        Raises:
            FileNotFoundError: If template file doesn't exist
            InvalidTemplateError: If template is malformed
            InvalidColorCodeError: If color codes are invalid
        """
        # Handle relative paths
        if not os.path.isabs(template_path):
            template_path = os.path.join(self.templates_dir, template_path)

        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if not isinstance(data, dict):
                raise InvalidTemplateError("Template must be a YAML dictionary")

            return self._build_template(data)

        except yaml.YAMLError as e:
            raise InvalidTemplateError(f"Invalid YAML syntax: {e}")
        except Exception as e:
            raise TemplateLoaderError(f"Failed to load template: {e}")

    def list_templates(self) -> List[Dict[str, str]]:
        """
        List all available templates in the templates directory

        Returns:
            List of template info dicts with 'name', 'path', 'description'
        """
        templates = []

        if not os.path.exists(self.templates_dir):
            return templates

        for file in os.listdir(self.templates_dir):
            if file.endswith('.yaml') or file.endswith('.yml'):
                file_path = os.path.join(self.templates_dir, file)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)

                    metadata = data.get('metadata', {})
                    templates.append({
                        'name': metadata.get('name', file),
                        'path': file_path,
                        'description': metadata.get('description', ''),
                        'use_case': metadata.get('use_case', '')
                    })
                except:
                    # Skip invalid files
                    continue

        return templates

    def _build_template(self, data: Dict) -> StyleTemplate:
        """Build StyleTemplate object from parsed YAML data"""

        template = StyleTemplate()

        # Metadata
        if 'metadata' in data:
            template.metadata = self._build_metadata(data['metadata'])

        # Colors
        if 'colors' in data:
            template.colors = self._build_colors(data['colors'])

        # Typography
        if 'typography' in data:
            template.typography = self._build_typography(data['typography'])

        # Layout
        if 'layout' in data:
            template.layout = self._build_layout(data['layout'])

        # Chart Elements
        if 'chart_elements' in data:
            template.chart_elements = self._build_chart_elements(data['chart_elements'])

        # Chart Types
        if 'chart_types' in data:
            template.chart_types = self._build_chart_types(data['chart_types'])

        # Filters
        if 'filters' in data:
            template.filters = self._build_filters(data['filters'])

        # Rules
        if 'rules' in data:
            template.rules = self._build_rules(data['rules'])

        # Notes
        if 'notes' in data:
            template.notes = str(data['notes'])

        return template

    def _build_metadata(self, data: Dict) -> Metadata:
        """Build Metadata from dict"""
        return Metadata(
            name=data.get('name', 'Unnamed Template'),
            description=data.get('description', ''),
            version=data.get('version', '1.0'),
            author=data.get('author', ''),
            created=data.get('created', ''),
            use_case=data.get('use_case', '')
        )

    def _build_colors(self, data: Dict) -> ColorPalette:
        """Build ColorPalette from dict with validation"""
        colors = ColorPalette()

        if 'brand' in data:
            colors.brand = self._validate_color_dict(data['brand'])

        if 'neutrals' in data:
            colors.neutrals = self._validate_color_dict(data['neutrals'])

        if 'categorical' in data:
            colors.categorical = self._validate_color_list(data['categorical'])

        if 'sequential' in data:
            seq = {}
            for key, palette in data['sequential'].items():
                seq[key] = self._validate_color_list(palette)
            colors.sequential = seq

        if 'diverging' in data:
            div = {}
            for key, palette in data['diverging'].items():
                div[key] = self._validate_color_list(palette)
            colors.diverging = div

        if 'semantic' in data:
            colors.semantic = self._validate_color_dict(data['semantic'])

        return colors

    def _build_typography(self, data: Dict) -> Typography:
        """Build Typography from dict"""
        typo = Typography()

        if 'title' in data:
            typo.title = self._build_typography_style(data['title'])

        if 'sheet_title' in data:
            typo.sheet_title = self._build_typography_style(data['sheet_title'])

        if 'body' in data:
            typo.body = self._build_typography_style(data['body'])

        if 'axis_labels' in data:
            typo.axis_labels = self._build_typography_style(data['axis_labels'])

        if 'data_labels' in data:
            typo.data_labels = self._build_typography_style(data['data_labels'])

        if 'tooltip' in data:
            typo.tooltip = self._build_typography_style(data['tooltip'])

        return typo

    def _build_typography_style(self, data: Dict) -> TypographyStyle:
        """Build TypographyStyle from dict"""
        style = TypographyStyle()

        if 'font_family' in data:
            style.font_family = str(data['font_family'])

        if 'font_size' in data:
            size = int(data['font_size'])
            if not (6 <= size <= 72):
                raise InvalidTemplateError(f"Font size {size} out of reasonable range (6-72)")
            style.font_size = size

        if 'font_weight' in data:
            style.font_weight = str(data['font_weight'])

        if 'color' in data:
            style.color = self._validate_color(data['color'])

        if 'alignment' in data:
            style.alignment = str(data['alignment'])

        return style

    def _build_layout(self, data: Dict) -> Layout:
        """Build Layout from dict"""
        layout = Layout()

        if 'dashboard' in data:
            d = data['dashboard']
            layout.dashboard = DashboardLayout(
                background_color=self._validate_color(d.get('background_color', '#FFFFFF')),
                padding=int(d.get('padding', 12))
            )

        if 'containers' in data:
            c = data['containers']
            layout.containers = ContainerLayout(
                background_color=self._validate_color(c.get('background_color', '#F2F2F2')),
                border_color=self._validate_color(c.get('border_color', '#D9D9D9')),
                border_width=int(c.get('border_width', 1)),
                padding=int(c.get('padding', 8)),
                spacing=int(c.get('spacing', 8))
            )

        if 'sheets' in data:
            s = data['sheets']
            layout.sheets = SheetLayout(
                background_color=self._validate_color(s.get('background_color', '#FFFFFF')),
                border_color=self._validate_color(s.get('border_color', '#D9D9D9')),
                border_width=int(s.get('border_width', 1)),
                padding=int(s.get('padding', 8)),
                title_background=self._validate_color(s.get('title_background', '#F2F2F2'))
            )

        return layout

    def _build_chart_elements(self, data: Dict) -> ChartElements:
        """Build ChartElements from dict"""
        elements = ChartElements()

        if 'gridlines' in data:
            g = data['gridlines']
            elements.gridlines = GridlineConfig(
                show=bool(g.get('show', True)),
                color=self._validate_color(g.get('color', '#D9D9D9')),
                style=str(g.get('style', 'solid')),
                opacity=float(g.get('opacity', 0.3))
            )

        if 'axes' in data:
            a = data['axes']
            elements.axes = AxisConfig(
                line_color=self._validate_color(a.get('line_color', '#6B6B6B')),
                line_width=int(a.get('line_width', 1)),
                show_zero_line=bool(a.get('show_zero_line', True)),
                zero_line_color=self._validate_color(a.get('zero_line_color', '#222222'))
            )

        if 'reference_lines' in data:
            r = data['reference_lines']
            elements.reference_lines = ReferenceLineConfig(
                color=self._validate_color(r.get('color', '#7E2D25')),
                style=str(r.get('style', 'dashed')),
                width=int(r.get('width', 2)),
                label_color=self._validate_color(r.get('label_color', '#7E2D25'))
            )

        if 'borders' in data:
            b = data['borders']
            elements.borders = BorderConfig(
                show=bool(b.get('show', True)),
                color=self._validate_color(b.get('color', '#D9D9D9')),
                width=int(b.get('width', 1))
            )

        if 'shadows' in data:
            elements.shadows = ShadowConfig(
                enabled=bool(data['shadows'].get('enabled', False))
            )

        if 'null_values' in data:
            n = data['null_values']
            elements.null_values = NullValueConfig(
                color=self._validate_color(n.get('color', '#D9D9D9')),
                pattern=str(n.get('pattern', 'diagonal-stripe'))
            )

        return elements

    def _build_chart_types(self, data: Dict) -> ChartTypes:
        """Build ChartTypes from dict"""
        types = ChartTypes()

        for chart_type in ['bar_chart', 'line_chart', 'pie_chart', 'map', 'heatmap', 'kpi_card']:
            if chart_type in data:
                config = self._build_chart_type_config(data[chart_type])
                setattr(types, chart_type, config)

        return types

    def _build_chart_type_config(self, data: Dict) -> ChartTypeConfig:
        """Build ChartTypeConfig from dict"""
        config = ChartTypeConfig()

        if 'default_color' in data:
            config.default_color = self._validate_color(data['default_color'])

        if 'border_color' in data:
            config.border_color = self._validate_color(data['border_color'])

        if 'use_categorical_palette' in data:
            config.use_categorical_palette = bool(data['use_categorical_palette'])

        # Store any additional properties
        config.properties = {k: v for k, v in data.items()
                            if k not in ['default_color', 'border_color', 'use_categorical_palette']}

        return config

    def _build_filters(self, data: Dict) -> FilterConfig:
        """Build FilterConfig from dict"""
        return FilterConfig(
            background_color=self._validate_color(data.get('background_color', '#F2F2F2')),
            border_color=self._validate_color(data.get('border_color', '#D9D9D9')),
            text_color=self._validate_color(data.get('text_color', '#222222')),
            highlight_color=self._validate_color(data.get('highlight_color', '#7E2D25')),
            dropdown_background=self._validate_color(data.get('dropdown_background', '#FFFFFF'))
        )

    def _build_rules(self, data: Dict) -> RulesConfig:
        """Build RulesConfig from dict"""
        rules = RulesConfig()

        if 'apply_to' in data:
            rules.apply_to = data['apply_to']

        if 'preserve_original' in data:
            rules.preserve_original = data['preserve_original']

        if 'quality' in data:
            rules.quality = data['quality']

        return rules

    def _validate_color(self, color: str) -> str:
        """Validate a hex color code"""
        if not self.COLOR_PATTERN.match(color):
            raise InvalidColorCodeError(
                f"Invalid color code: {color}. Expected format: #RRGGBB"
            )
        return color

    def _validate_color_dict(self, colors: Dict[str, str]) -> Dict[str, str]:
        """Validate all colors in a dictionary"""
        validated = {}
        for key, color in colors.items():
            validated[key] = self._validate_color(color)
        return validated

    def _validate_color_list(self, colors: List[str]) -> List[str]:
        """Validate all colors in a list"""
        return [self._validate_color(c) for c in colors]
