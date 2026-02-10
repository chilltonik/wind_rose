import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from wind_rose.config import ChartConfig, FontSizes


def plot_radar(
    month_name: str, categories: dict[str, int], year: int, config: ChartConfig
) -> Figure:
    """Build a radar (polar) chart for a single month.

    Args:
        month_name: Name of the month.
        categories: Mapping of category names to scores.
        year: The data year (used in the title).
        config: Chart configuration.

    Returns:
        Matplotlib Figure with the radar chart.
    """
    fs: FontSizes = config.font_sizes
    measure: int = config.measure
    names: list[str] = list(categories.keys())
    values: list[int] = list(categories.values())

    fig, ax = plt.subplots(
        figsize=(12, 10), subplot_kw={"projection": "polar"}
    )

    angles: list[float] = np.linspace(
        0, 2 * np.pi, len(names), endpoint=False
    ).tolist()
    angles += angles[:1]
    values_plot: list[int] = values + values[:1]

    ax.plot(
        angles, values_plot, "o-", linewidth=3, markersize=8, color="#2E86AB"
    )
    ax.fill(angles, values_plot, alpha=0.25, color="#2E86AB")

    target_circle = np.linspace(0, 2 * np.pi, 100)
    ax.plot(
        target_circle,
        [measure] * 100,
        "--",
        color="red",
        alpha=0.3,
        linewidth=1,
    )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(names, fontsize=fs.tick_label)
    ax.set_ylim(0, measure + 1)
    ax.grid(True, alpha=0.3)

    avg_value: np.floating = np.mean(values)
    completion: float = sum(values) / (len(values) * measure) * 100

    stats_text: str = f"Mean: {avg_value:.1f}/{measure}\n"
    stats_text += f"Max: {max(values)}/{measure}\n"
    stats_text += f"Min: {min(values)}/{measure}\n"
    stats_text += f"Feeling: {completion:.1f}%"

    ax.text(
        0,
        0,
        stats_text,
        ha="center",
        va="center",
        fontsize=fs.stats_text,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.9),
    )

    title: str = f"{config.diagram_name}\n{month_name}"
    if year:
        title += f" {year}"
    plt.title(title, fontsize=fs.title, pad=20)
    plt.tight_layout()

    return fig
