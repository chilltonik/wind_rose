import json
import logging
from logging import Logger
from pathlib import Path

from pydantic import BaseModel, Field

logger: Logger = logging.getLogger(__name__)


class FontSizes(BaseModel):
    """Font size settings used across all chart types."""

    title: int = Field(default=16, description="Main chart title font size")
    subtitle: int = Field(default=14, description="Subplot title font size")
    axis_label: int = Field(default=12, description="X/Y axis label font size")
    tick_label: int = Field(
        default=16, description="Tick label font size on axes"
    )
    stats_text: int = Field(
        default=16,
        description="Statistics text font size in radar chart center",
    )
    bar_value: int = Field(
        default=14,
        description="Value label font size above bars in comparison chart",
    )


class ChartConfig(BaseModel):
    """Top-level configuration loaded from chart_config.json."""

    diagram_name: str = Field(
        default="Diagram name",
        description="Title displayed on the radar chart",
    )
    measure: int = Field(
        default=10, description="Maximum score on the rating scale"
    )
    year: int = Field(default=2026, description="Data year")
    data_path: str = Field(
        default="data/life_directions.json",
        description="Path to the JSON data file",
    )
    output_dir: str = Field(
        default="images/life_directions",
        description="Directory for saved chart images",
    )
    font_sizes: FontSizes = Field(
        default_factory=FontSizes,
        description="Font size settings for all chart elements",
    )


def load_chart_config(
    config_path: str = "config/chart_config.json",
) -> ChartConfig:
    """Load chart configuration from a JSON file.

    Falls back to default values if the file is missing or invalid.

    Args:
        config_path: Path to the JSON configuration file.

    Returns:
        Validated ChartConfig instance.
    """
    path: Path = Path(config_path)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            raw: dict[str, object] = json.load(f)
        config = ChartConfig.model_validate(raw)
        logger.info("Chart config loaded from %s", config_path)
        return config
    logger.warning("Config not found at %s, using defaults", config_path)
    return ChartConfig()
