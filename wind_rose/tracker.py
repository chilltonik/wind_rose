import json
import logging
import os

from matplotlib.figure import Figure

from wind_rose.config import ChartConfig, load_chart_config
from wind_rose.plots import plot_comparison, plot_radar, plot_summary

logger = logging.getLogger(__name__)


class LifeBalanceTracker:
    """Life balance tracker with yearly goal visualizations.

    Loads monthly rating data from JSON files and produces charts:
    radar diagram, month-to-month comparison, and yearly summary.
    """

    def __init__(
        self,
        year: int,
        data_path: str = "data",
        config: ChartConfig | None = None,
    ) -> None:
        self.data_path: str = data_path
        self.year: int = year
        self.config: ChartConfig = config or load_chart_config()

        self.data: dict[str, dict[str, int]] = self.load_data()

    def load_data(self) -> dict[str, dict[str, int]]:
        """Load rating data from the JSON file for the current year.

        Returns:
            Mapping of month names to category-score pairs.
        """
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                data: dict[str, dict[str, int]] = json.load(f)
                logger.info("Data loaded from %s", self.data_path)
                return data
        except Exception as e:
            logger.error("Error during loading %s: %s", self.data_path, e)
            return {}

    def get_available_months(self, year: int | None = None) -> list[str]:
        """Return a list of months with data for the given or current year.

        Args:
            year: Year to query. Uses the current year if None.

        Returns:
            List of month name strings.
        """
        if year and year != self.year:
            temp_file: str = os.path.join(
                self.data_path, f"life_data_{year}.json"
            )
            if os.path.exists(temp_file):
                with open(temp_file, "r", encoding="utf-8") as f:
                    data: dict[str, dict[str, int]] = json.load(f)
                return list(data.keys())
            else:
                return []
        else:
            return list(self.data.keys())

    def plot_current_month(self, month_name: str) -> Figure | None:
        """Build a radar (polar) chart for a single month.

        Args:
            month_name: Name of the month as it appears in the data file.

        Returns:
            Matplotlib Figure or None if the month is not found.
        """
        if month_name not in self.data:
            logger.warning("Data for %s is not found", month_name)
            return None

        return plot_radar(
            month_name=month_name,
            categories=self.data[month_name],
            year=self.year,
            config=self.config,
        )

    def plot_month_comparison(
        self, months_to_compare: list[str]
    ) -> Figure | None:
        """Build a grouped bar chart comparing several months.

        Args:
            months_to_compare: List of month names to include.

        Returns:
            Matplotlib Figure or None if any month is missing.
        """
        missing_months: list[str] = [
            m for m in months_to_compare if m not in self.data
        ]
        if missing_months:
            logger.warning("Data for months is not found: %s", missing_months)
            return None

        months_data = {m: self.data[m] for m in months_to_compare}
        return plot_comparison(
            months_data=months_data, year=self.year, config=self.config
        )

    def plot_yearly_summary(self) -> Figure | None:
        """Build a yearly summary with a heatmap and mean-value trend line.

        Returns:
            Matplotlib Figure or None if no data is available.
        """
        if not self.data:
            logger.warning("No data for plotting")
            return None

        return plot_summary(data=self.data, year=self.year, config=self.config)
