"""Life weeks visualization.

Renders a 100×52 grid (years × weeks) — 5200 weeks total.

Usage:
    python3 weeks.py 1211           # dark style (default)
    python3 weeks.py 1211 light     # light style
    python3 weeks.py 1211 dark      # dark style
    python3 weeks.py                # no week highlighted
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

YEARS = 100
WEEKS_PER_ROW = 52


# ── theme definitions ────────────────────────────────────────────────────────


@dataclass
class Theme:
    bg: str
    panel: str  # grid background
    past_a: str  # gradient start (early weeks)
    past_b: str  # gradient end (recent weeks)
    future: str
    future_border: str  # subtle border on empty cells
    current: str
    label: str  # axis labels
    title: str
    subtitle: str
    bar_done: str
    bar_todo: str


DARK = Theme(
    bg="#111114",
    panel="#111114",
    past_a="#2563b0",  # deep blue – early
    past_b="#16a34a",  # forest green – later
    future="#1c1c22",
    future_border="#2a2a36",
    current="#facc15",  # gold
    label="#3d3d52",
    title="#d4d4e8",
    subtitle="#4a4a62",
    bar_done="#2563b0",
    bar_todo="#22222e",
)

LIGHT = Theme(
    bg="#f5f4f0",
    panel="#f5f4f0",
    past_a="#1d4ed8",  # royal blue – early
    past_b="#15803d",  # deep green – later
    future="#dddbd5",
    future_border="#c8c5bc",
    current="#dc2626",  # red accent
    label="#9a9888",
    title="#1a1a2e",
    subtitle="#7a7868",
    bar_done="#1d4ed8",
    bar_todo="#ccc9c0",
)

THEMES: dict[str, Theme] = {"dark": DARK, "light": LIGHT}


# ── helpers ──────────────────────────────────────────────────────────────────


def _hex_to_rgb(h: str) -> tuple[float, float, float]:
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]


def _lerp(
    c1: tuple[float, ...], c2: tuple[float, ...], t: float
) -> tuple[float, float, float]:
    return tuple(c1[i] + (c2[i] - c1[i]) * t for i in range(3))  # type: ignore[return-value]


# ── drawing ──────────────────────────────────────────────────────────────────


def _draw_grid(
    ax: plt.Axes, theme: Theme, current_week: int | None, total_weeks: int
) -> None:
    past_rgb = _hex_to_rgb(theme.past_a)
    maturity_rgb = _hex_to_rgb(theme.past_b)
    future_rgb = _hex_to_rgb(theme.future)
    future_border_rgb = _hex_to_rgb(theme.future_border)
    current_rgb = _hex_to_rgb(theme.current)

    cell_fill = 0.72  # filled cell size (gap = 0.28 of cell)
    future_fill = 0.65  # empty cell slightly smaller
    radius = 0.07  # corner rounding

    for year_idx in range(YEARS):
        row = YEARS - 1 - year_idx
        for week_idx in range(WEEKS_PER_ROW):
            absolute = year_idx * WEEKS_PER_ROW + week_idx
            cx = week_idx + 0.5
            cy = row + 0.5

            is_current = current_week is not None and absolute == current_week
            is_past = current_week is not None and absolute < current_week

            if is_current:
                size = cell_fill * 1.18
                color = current_rgb
                alpha = 1.0
                lw = 0
                ec = None
            elif is_past:
                t = absolute / max(current_week, 1)  # type: ignore
                color = _lerp(past_rgb, maturity_rgb, t)
                alpha = 0.45 + 0.55 * (t**0.35)
                size = cell_fill
                lw = 0
                ec = None
            else:
                color = future_rgb
                alpha = 1.0
                size = future_fill
                lw = 0.4  # type: ignore
                ec = future_border_rgb

            rect = mpatches.FancyBboxPatch(
                (cx - size / 2, cy - size / 2),
                size,
                size,
                boxstyle=f"round,pad={radius}",
                linewidth=lw,
                edgecolor=ec,
                facecolor=color,
                alpha=alpha,
                zorder=2,
            )
            ax.add_patch(rect)

            # decade marker: thin horizontal line above row 10, 20, ...
            if week_idx == 0 and year_idx > 0 and year_idx % 10 == 0:
                ax.plot(
                    [0, WEEKS_PER_ROW],
                    [row + 1, row + 1],
                    color=_hex_to_rgb(theme.subtitle),
                    linewidth=0.4,
                    alpha=0.4,
                    zorder=1,
                )


def _draw_labels(ax: plt.Axes, theme: Theme) -> None:
    lc = theme.label
    for year_idx in range(YEARS):
        row = YEARS - 1 - year_idx
        if year_idx % 5 == 0:
            label = str(year_idx) if year_idx > 0 else "0"
            ax.text(
                -0.45,
                row + 0.5,
                label,
                ha="right",
                va="center",
                fontsize=5,
                color=lc,
                fontfamily="monospace",
            )
            # right side: every 10
            if year_idx % 10 == 0:
                ax.text(
                    WEEKS_PER_ROW + 0.45,
                    row + 0.5,
                    str(year_idx),
                    ha="left",
                    va="center",
                    fontsize=5,
                    color=lc,
                    fontfamily="monospace",
                )

    for w in range(0, WEEKS_PER_ROW, 4):
        ax.text(
            w + 0.5,
            -0.55,
            str(w + 1),
            ha="center",
            va="top",
            fontsize=4.5,
            color=lc,
            fontfamily="monospace",
        )


def _draw_header(
    fig: plt.Figure,
    theme: Theme,
    current_week: int | None,
    total_weeks: int,
    fig_h_pts: float,
) -> None:
    # use display points from top so positions don't shift with fig height
    def _y(pts_from_top: float) -> float:
        return 1.0 - pts_from_top / fig_h_pts

    fig.text(
        0.5,
        _y(10),
        "100  YEARS  IN  WEEKS",
        ha="center",
        va="top",
        fontsize=10,
        color=theme.title,
        fontfamily="monospace",
        fontweight="bold",
        transform=fig.transFigure,
    )

    if current_week is None:
        fig.text(
            0.5,
            _y(35),
            f"{total_weeks} weeks  ·  {YEARS} years",
            ha="center",
            va="top",
            fontsize=6,
            color=theme.subtitle,
            fontfamily="monospace",
            transform=fig.transFigure,
        )
        return

    weeks_done = current_week + 1
    weeks_left = total_weeks - weeks_done
    pct = weeks_done / total_weeks * 100
    year_num = weeks_done // WEEKS_PER_ROW + 1
    week_in_year = weeks_done % WEEKS_PER_ROW or WEEKS_PER_ROW

    fig.text(
        0.5,
        _y(35),
        f"неделя  {weeks_done}  /  {total_weeks}",
        ha="center",
        va="top",
        fontsize=8,
        color=theme.subtitle,
        fontfamily="monospace",
        fontweight="bold",
        transform=fig.transFigure,
    )
    fig.text(
        0.5,
        _y(57),
        f"year {year_num} week {week_in_year} left {weeks_left} weeks",
        ha="center",
        va="top",
        fontsize=5.5,
        color=theme.subtitle,
        fontfamily="monospace",
        transform=fig.transFigure,
    )

    # progress bar — drawn at fixed offset from top
    bar_y = _y(74)
    bar_w = 50
    filled = round(pct / 100 * bar_w)
    done_c = _hex_to_rgb(theme.bar_done)
    todo_c = _hex_to_rgb(theme.bar_todo)
    step = 0.006
    x0 = 0.5 - bar_w * step / 2
    for i in range(bar_w):
        color = done_c if i < filled else todo_c
        fig.text(
            x0 + i * step,
            bar_y,
            "█",
            ha="left",
            va="top",
            fontsize=4.8,
            color=color,
            fontfamily="monospace",
            transform=fig.transFigure,
        )
    fig.text(
        x0 + bar_w * step + 0.005,
        bar_y,
        f"{pct:.1f}%",
        ha="left",
        va="top",
        fontsize=4.5,
        color=theme.subtitle,
        fontfamily="monospace",
        transform=fig.transFigure,
    )


# ── main ─────────────────────────────────────────────────────────────────────


def main() -> None:
    args = sys.argv[1:]

    current_week: int | None = None
    theme_name = "dark"

    for arg in args:
        if arg in THEMES:
            theme_name = arg
        else:
            try:
                w = int(arg)
                current_week = max(0, w - 1)
            except ValueError:
                pass

    theme = THEMES[theme_name]
    total_weeks = YEARS * WEEKS_PER_ROW

    cell = 14
    pad_left = 34
    pad_bottom = 28
    pad_top = 110
    pad_right = 24

    fig_w = (WEEKS_PER_ROW * cell + pad_left + pad_right) / 72
    fig_h = (YEARS * cell + pad_top + pad_bottom) / 72

    fig = plt.figure(figsize=(fig_w, fig_h), dpi=144, facecolor=theme.bg)

    ax = fig.add_axes([
        pad_left / (fig_w * 72),
        pad_bottom / (fig_h * 72),
        WEEKS_PER_ROW * cell / (fig_w * 72),
        YEARS * cell / (fig_h * 72),
    ])
    ax.set_facecolor(theme.panel)
    ax.set_xlim(0, WEEKS_PER_ROW)
    ax.set_ylim(0, YEARS)
    ax.set_aspect("equal")
    ax.axis("off")

    fig_h_pts = fig_h * 72
    _draw_grid(ax, theme, current_week, total_weeks)
    _draw_labels(ax, theme)
    _draw_header(fig, theme, current_week, total_weeks, fig_h_pts)

    out = f"images/weeks_{theme_name}.png"
    plt.savefig(out, dpi=144, bbox_inches="tight", facecolor=theme.bg)
    print(f"Saved → {out}")
    plt.show()


# python3 weeks.py 1211 light |& tee logs/weeks.log
if __name__ == "__main__":
    main()
