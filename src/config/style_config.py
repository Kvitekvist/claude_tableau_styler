"""
Style Configuration Data Models

Represents a loaded style template configuration.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class ColorPalette:
    """Color palette configuration"""
    # Brand colors
    brand: Dict[str, str] = field(default_factory=dict)

    # Neutral colors
    neutrals: Dict[str, str] = field(default_factory=dict)

    # Categorical palette (for dimensions)
    categorical: List[str] = field(default_factory=list)

    # Sequential palette (for continuous measures)
    sequential: Dict[str, List[str]] = field(default_factory=dict)

    # Diverging palette (for variance)
    diverging: Dict[str, List[str]] = field(default_factory=dict)

    # Semantic colors
    semantic: Dict[str, str] = field(default_factory=dict)


@dataclass
class TypographyStyle:
    """Typography configuration for a specific element type"""
    font_family: str = "Arial"
    font_size: int = 11
    font_weight: str = "normal"
    color: str = "#222222"
    alignment: str = "left"


@dataclass
class Typography:
    """Typography configuration"""
    title: TypographyStyle = field(default_factory=lambda: TypographyStyle(
        font_size=20, font_weight="bold"
    ))
    sheet_title: TypographyStyle = field(default_factory=lambda: TypographyStyle(
        font_size=14, font_weight="bold"
    ))
    body: TypographyStyle = field(default_factory=TypographyStyle)
    axis_labels: TypographyStyle = field(default_factory=lambda: TypographyStyle(
        font_size=10, color="#6B6B6B"
    ))
    data_labels: TypographyStyle = field(default_factory=lambda: TypographyStyle(
        font_size=10
    ))
    tooltip: TypographyStyle = field(default_factory=TypographyStyle)


@dataclass
class DashboardLayout:
    """Dashboard layout configuration"""
    background_color: str = "#FFFFFF"
    padding: int = 12


@dataclass
class ContainerLayout:
    """Container layout configuration"""
    background_color: str = "#F2F2F2"
    border_color: str = "#D9D9D9"
    border_width: int = 1
    padding: int = 8
    spacing: int = 8


@dataclass
class SheetLayout:
    """Sheet/worksheet layout configuration"""
    background_color: str = "#FFFFFF"
    border_color: str = "#D9D9D9"
    border_width: int = 1
    padding: int = 8
    title_background: str = "#F2F2F2"


@dataclass
class Layout:
    """Layout configuration"""
    dashboard: DashboardLayout = field(default_factory=DashboardLayout)
    containers: ContainerLayout = field(default_factory=ContainerLayout)
    sheets: SheetLayout = field(default_factory=SheetLayout)


@dataclass
class GridlineConfig:
    """Gridline configuration"""
    show: bool = True
    color: str = "#D9D9D9"
    style: str = "solid"  # solid, dashed, dotted
    opacity: float = 0.3


@dataclass
class AxisConfig:
    """Axis configuration"""
    line_color: str = "#6B6B6B"
    line_width: int = 1
    show_zero_line: bool = True
    zero_line_color: str = "#222222"


@dataclass
class ReferenceLineConfig:
    """Reference line configuration"""
    color: str = "#7E2D25"
    style: str = "dashed"
    width: int = 2
    label_color: str = "#7E2D25"


@dataclass
class BorderConfig:
    """Border configuration"""
    show: bool = True
    color: str = "#D9D9D9"
    width: int = 1


@dataclass
class ShadowConfig:
    """Shadow configuration"""
    enabled: bool = False


@dataclass
class NullValueConfig:
    """Null value configuration"""
    color: str = "#D9D9D9"
    pattern: str = "diagonal-stripe"


@dataclass
class ChartElements:
    """Chart elements configuration"""
    gridlines: GridlineConfig = field(default_factory=GridlineConfig)
    axes: AxisConfig = field(default_factory=AxisConfig)
    reference_lines: ReferenceLineConfig = field(default_factory=ReferenceLineConfig)
    borders: BorderConfig = field(default_factory=BorderConfig)
    shadows: ShadowConfig = field(default_factory=ShadowConfig)
    null_values: NullValueConfig = field(default_factory=NullValueConfig)


@dataclass
class ChartTypeConfig:
    """Configuration for specific chart types"""
    default_color: str = "#7E2D25"
    border_color: Optional[str] = None
    use_categorical_palette: bool = True
    # Additional chart-specific properties as Dict
    properties: Dict[str, any] = field(default_factory=dict)


@dataclass
class ChartTypes:
    """Chart type specific configurations"""
    bar_chart: ChartTypeConfig = field(default_factory=ChartTypeConfig)
    line_chart: ChartTypeConfig = field(default_factory=ChartTypeConfig)
    pie_chart: ChartTypeConfig = field(default_factory=ChartTypeConfig)
    map: ChartTypeConfig = field(default_factory=ChartTypeConfig)
    heatmap: ChartTypeConfig = field(default_factory=ChartTypeConfig)
    kpi_card: ChartTypeConfig = field(default_factory=ChartTypeConfig)


@dataclass
class FilterConfig:
    """Filter control configuration"""
    background_color: str = "#F2F2F2"
    border_color: str = "#D9D9D9"
    text_color: str = "#222222"
    highlight_color: str = "#7E2D25"
    dropdown_background: str = "#FFFFFF"


@dataclass
class RulesConfig:
    """Styling application rules"""
    apply_to: List[str] = field(default_factory=lambda: [
        "titles", "highlights", "tooltips", "filters", "reference_lines"
    ])
    preserve_original: List[str] = field(default_factory=lambda: [
        "custom_calculations", "explicit_color_legends"
    ])
    quality: Dict[str, bool] = field(default_factory=lambda: {
        "anti_aliasing": True,
        "font_smoothing": True,
        "high_quality_export": True
    })


@dataclass
class Metadata:
    """Template metadata"""
    name: str = "Unnamed Template"
    description: str = ""
    version: str = "1.0"
    author: str = ""
    created: str = ""
    use_case: str = ""


@dataclass
class StyleTemplate:
    """Complete style template configuration"""
    metadata: Metadata = field(default_factory=Metadata)
    colors: ColorPalette = field(default_factory=ColorPalette)
    typography: Typography = field(default_factory=Typography)
    layout: Layout = field(default_factory=Layout)
    chart_elements: ChartElements = field(default_factory=ChartElements)
    chart_types: ChartTypes = field(default_factory=ChartTypes)
    filters: FilterConfig = field(default_factory=FilterConfig)
    rules: RulesConfig = field(default_factory=RulesConfig)
    notes: str = ""
