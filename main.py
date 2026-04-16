import argparse
import os

from matplotlib.figure import Figure

from wind_rose import (
    ChartConfig,
    LifeBalanceTracker,
    load_chart_config,
    setup_logging,
)

CONFIGS: dict[str, str] = {
    "life_directions": "config/life_directions.json",
    "year_goals": "config/year_goals.json",
}


def select_config() -> str:
    names = list(CONFIGS)
    print("Select config:")
    for i, name in enumerate(names, 1):
        print(f"  {i}. {name}")
    choice = input("Enter name or number: ").strip()
    if choice in CONFIGS:
        return CONFIGS[choice]
    try:
        return CONFIGS[names[int(choice) - 1]]
    except (ValueError, IndexError):
        raise SystemExit(f"Invalid choice: {choice!r}")


def parse_config_path() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "config",
        nargs="?",
        choices=list(CONFIGS),
        help="Config name: " + " | ".join(CONFIGS),
    )
    args = parser.parse_args()
    return CONFIGS[args.config] if args.config else select_config()


def main() -> None:
    setup_logging()
    config_path = parse_config_path()
    config: ChartConfig = load_chart_config(config_path)

    tracker: LifeBalanceTracker = LifeBalanceTracker(
        data_path=config.data_path, year=config.year, config=config
    )

    os.makedirs(config.output_dir, exist_ok=True)

    figures: dict[str, Figure | None] = {
        "current_month.png": tracker.plot_current_month("April"),
        "month_comparison.png": tracker.plot_month_comparison([
            "January",
            "February",
            "March",
            "April",
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
