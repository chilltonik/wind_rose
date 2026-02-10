import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

from wind_rose.config import ChartConfig, FontSizes


def plot_summary(
    data: dict[str, dict[str, int]], year: int, config: ChartConfig
) -> Figure:
    """Build a yearly summary with a heatmap and mean-value trend line.

    Args:
        data: Mapping of month names to their category-score pairs.
        year: The data year (used in the title).
        config: Chart configuration.

    Returns:
        Matplotlib Figure with the summary charts.
    """
    fs: FontSizes = config.font_sizes
    measure: int = config.measure
    months: list[str] = list(data.keys())
    categories: list[str] = list(data[months[0]].keys())

    data_rows: list[list[int]] = []
    for month in months:
        month_data: dict[str, int] = data[month]
        values: list[int] = [month_data.get(cat, 0) for cat in categories]
        data_rows.append(values)

    data_matrix = np.array(data_rows)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))

    im = ax1.imshow(
        data_matrix.T, aspect="auto", cmap="YlGnBu", vmin=0, vmax=measure
    )

    ax1.set_xticks(range(len(months)))
    ax1.set_xticklabels(months, rotation=45, ha="right")
    ax1.set_yticks(range(len(categories)))
    ax1.set_yticklabels(categories)
    ax1.set_title(f"Progress heatmap for {year}", fontsize=fs.subtitle, pad=20)

    for i in range(len(months)):
        for j in range(len(categories)):
            value = data_matrix[i, j]
            color: str = "white" if value > 6 else "black"
            ax1.text(
                i,
                j,
                str(int(value)),
                ha="center",
                va="center",
                color=color,
                fontweight="bold",
            )

    plt.colorbar(im, ax=ax1, label="Values")

    monthly_means = np.mean(data_matrix, axis=1)
    monthly_max = np.max(data_matrix, axis=1)
    monthly_min = np.min(data_matrix, axis=1)

    ax2.plot(
        months,
        monthly_means,
        "o-",
        linewidth=2,
        markersize=8,
        label="Mean",
        color="blue",
    )
    ax2.fill_between(months, monthly_min, monthly_max, alpha=0.2, color="blue")

    ax2.set_xlabel("Month", fontsize=fs.axis_label)
    ax2.set_ylabel("Value", fontsize=fs.axis_label)
    ax2.set_title(
        "Mean values dynamics by months", fontsize=fs.subtitle, pad=20
    )
    ax2.set_ylim(0, measure + 1)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    return fig
