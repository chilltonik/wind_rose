import numpy as np
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

plt.title(
    "Life directions",
    va="bottom",
    fontsize=18,
    color="black",
    fontweight="bold",
    pad=50,
)

plt.savefig(f"{name}.png", dpi=300, bbox_inches="tight")
plt.show()
