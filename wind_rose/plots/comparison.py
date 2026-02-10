import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from wind_rose.config import ChartConfig, FontSizes


def plot_comparison(
    months_data: dict[str, dict[str, int]], year: int, config: ChartConfig
) -> Figure:
    """Build a grouped bar chart comparing several months.

    Args:
        months_data: Mapping of month names to their category-score pairs.
        year: The data year (used in the title).
        config: Chart configuration.

    Returns:
        Matplotlib Figure with the comparison chart.
    """
    fs: FontSizes = config.font_sizes
    measure: int = config.measure
    months_to_compare: list[str] = list(months_data.keys())

    fig, ax = plt.subplots(figsize=(14, 8))
    colors = plt.cm.Set2(np.linspace(0, 1, len(months_to_compare)))

    first_month: str = months_to_compare[0]
    categories: list[str] = list(months_data[first_month].keys())

    bar_width: float = 0.15
    x = np.arange(len(categories))

    for idx, month in enumerate(months_to_compare):
        values: list[int] = list(months_data[month].values())

        offset: float = (
            idx - len(months_to_compare) / 2
        ) * bar_width + bar_width / 2

        bars = ax.bar(
            x + offset,
            values,
            width=bar_width,
            label=month,
            color=colors[idx],
            alpha=0.8,
            edgecolor="black",
        )

        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height + 0.1,
                f"{value}",
                ha="center",
                va="bottom",
                fontsize=fs.bar_value,
                fontweight="bold",
            )

    ax.set_xlabel("Categories", fontsize=fs.axis_label)
    ax.set_ylabel("Values", fontsize=fs.axis_label)

    title: str = "Months comparison"
    if year:
        title += f" {year}"
    ax.set_title(title, fontsize=fs.title, pad=20)

    ax.set_xticks(x)
    ax.set_xticklabels(
        categories, rotation=45, ha="right", fontsize=fs.tick_label
    )
    ax.set_ylim(0, measure + 1)
    ax.axhline(
        y=measure, color="red", linestyle="--", alpha=0.3, label="Target"
    )
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
    ax.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    return fig
