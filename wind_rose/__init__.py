import logging

from wind_rose.config import ChartConfig, load_chart_config
from wind_rose.tracker import LifeBalanceTracker

__all__: list[str] = [
    "ChartConfig",
    "LifeBalanceTracker",
    "load_chart_config",
    "setup_logging",
]


def setup_logging(level: int = logging.INFO) -> None:
    """Configure logging for the wind_rose package."""
    logger = logging.getLogger("wind_rose")
    if logger.handlers:
        return
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logger.addHandler(handler)
