import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

from data import data, name, max_measure

color = "black"

angles = np.linspace(0, 2 * np.pi, len(data.keys()), endpoint=False).tolist()
angles += angles[:1]

values = list(data.values())
values += values[:1]

fig, ax = plt.subplots(figsize=(9, 9), subplot_kw={"polar": True})

ax.fill(angles, values, color="#88c999", alpha=0.6)
ax.plot(angles, values, color="#2a9d8f", linewidth=3)

ax.set_yticks(range(0, max_measure + 1, 1))
ax.set_yticklabels(
    [str(i) for i in range(0, max_measure + 1, 1)], color=color, fontsize=10, fontweight="bold"
)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(data.keys(), fontsize=12, color=color, fontweight="bold")

ax.grid(color=color, linestyle="--", linewidth=0.8, alpha=0.7)

for spine in ax.spines.values():
    spine.set_edgecolor("lightgray")

ax.set_facecolor("white")
ax.tick_params(axis="both", which="major", pad=5)

def calculate_polygon_area(angles, values):
    x = values * np.cos(angles)
    y = values * np.sin(angles)
    area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
    return area

area = calculate_polygon_area(np.array(angles), np.array(values))

ax.text(0, 0, f"{area:.1f}",
        ha='center', va='center',
        fontsize=20, fontweight='bold',
        color='black')

plt.title(
    name,
    va="bottom",
    fontsize=18,
    color="black",
    fontweight="bold",
    pad=50,
)

plt.savefig(f"{name}.png", dpi=300, bbox_inches="tight")
plt.show()