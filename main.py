import os

from matplotlib.figure import Figure

from wind_rose import (
    ChartConfig,
    LifeBalanceTracker,
    load_chart_config,
    setup_logging,
)


def main() -> None:
    setup_logging()
    config: ChartConfig = load_chart_config()

    tracker: LifeBalanceTracker = LifeBalanceTracker(
        data_path=config.data_path, year=config.year, config=config
    )

    os.makedirs(config.output_dir, exist_ok=True)

    figures: dict[str, Figure | None] = {
        "current_month.png": tracker.plot_current_month("February"),
        "month_comparison.png": tracker.plot_month_comparison([
            "January",
            "February",
        ]),
        "yearly_summary.png": tracker.plot_yearly_summary(),
    }
    for filename, fig in figures.items():
        if fig:
            fig.savefig(
                os.path.join(config.output_dir, filename),
                dpi=150,
                bbox_inches="tight",
            )


# python3 main.py |& tee logs/main.log
if __name__ == "__main__":
    main()
