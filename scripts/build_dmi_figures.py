"""Draw the two DMI figures from the small CSV files that are in git.

The closure bundle does not contain the original multi-panel DMI diagnostics.
These figures show only the SON series and the ranked events in those tables.
They do not add box plots or the scatter panels that are still only on Lengau.

    python scripts/build_dmi_figures.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
FIG = REPO / "manuscript" / "figures"
ANNUAL = REPO / "dmi_son_annual_averages.csv"
EVENTS = REPO / "dmi_son_top_events.csv"

# Okabe–Ito, distinguished by colour and line style.
SERIES = (
    ("DMI_HadISST_SON", "HadISST", "#0072B2", "-"),
    ("DMI_ERSST_SON", "ERSST v5", "#E69F00", "--"),
    ("DMI_ERA5_SON", "ERA5", "#009E73", "-."),
)


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    annual = pd.read_csv(ANNUAL)
    events = pd.read_csv(EVENTS)

    fig, ax = plt.subplots(figsize=(7.2, 3.6), layout="constrained")
    for column, label, color, style in SERIES:
        ax.plot(
            annual["Year"],
            annual[column],
            color=color,
            linestyle=style,
            linewidth=1.4,
            label=label,
        )
    ax.axhline(0.0, color="#666666", linewidth=0.6)
    ax.set_xlim(1980, 2020)
    ax.set_xlabel("Year")
    ax.set_ylabel("SON DMI (°C)")
    ax.legend(frameon=False, ncol=3)
    fig.savefig(FIG / "dmi_son_series.png", dpi=200)
    plt.close(fig)

    positive = events[events["Event_Type"] == "Positive"].sort_values("Rank")
    negative = events[events["Event_Type"] == "Negative"].sort_values("Rank")
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.8), sharey=True, layout="constrained")
    for ax, sample, title in (
        (axes[0], positive, "Strongest positive SON events"),
        (axes[1], negative, "Strongest negative SON events"),
    ):
        y = range(len(sample))
        ax.barh(
            [i - 0.25 for i in y],
            sample["HadISST_DMI"],
            height=0.22,
            color="#0072B2",
            label="HadISST",
        )
        ax.barh(
            list(y),
            sample["ERSST_DMI"],
            height=0.22,
            color="#E69F00",
            label="ERSST v5",
        )
        ax.barh(
            [i + 0.25 for i in y],
            sample["ERA5_DMI"],
            height=0.22,
            color="#009E73",
            label="ERA5",
        )
        ax.set_yticks(list(y), [str(int(year)) for year in sample["Year"]])
        ax.axvline(0.0, color="#666666", linewidth=0.6)
        ax.set_xlabel("SON DMI (°C)")
        ax.set_title(title)
    axes[0].legend(frameon=False, loc="lower right")
    fig.savefig(FIG / "dmi_son_events.png", dpi=200)
    plt.close(fig)
    print(f"wrote {FIG / 'dmi_son_series.png'}")
    print(f"wrote {FIG / 'dmi_son_events.png'}")


if __name__ == "__main__":
    main()
