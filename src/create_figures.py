"""Generate portfolio-ready figures from the processed marts."""

from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd

try:
    from .config import FIGURES_DIR, MIN_COMPANY_COMPLAINTS, PROCESSED_DIR
except ImportError:  # Direct script execution
    from config import FIGURES_DIR, MIN_COMPANY_COMPLAINTS, PROCESSED_DIR


NAVY = "#14213D"
BLUE = "#0077B6"
TEAL = "#00A896"
ORANGE = "#F4A261"
RED = "#E76F51"
GRAY = "#5B6573"


def _style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#D8DEE8",
            "axes.titlecolor": NAVY,
            "axes.labelcolor": GRAY,
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titleweight": "bold",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "grid.color": "#E9EDF2",
            "grid.linewidth": 0.8,
        }
    )


def create() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    _style()

    monthly = pd.read_csv(PROCESSED_DIR / "fact_monthly.csv")
    monthly["month_date"] = pd.to_datetime(monthly["month"] + "-01")
    fig, left = plt.subplots(figsize=(12, 6.5))
    left.plot(monthly["month_date"], monthly["complaint_count"], color=BLUE, marker="o", linewidth=2.6)
    left.fill_between(monthly["month_date"], monthly["complaint_count"], color=BLUE, alpha=0.08)
    left.set_ylabel("Complaints", color=BLUE)
    left.yaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
    left.grid(axis="y")
    right = left.twinx()
    right.plot(monthly["month_date"], 1 - monthly["timely_rate"], color=RED, marker="s", linewidth=2.2)
    right.set_ylabel("Untimely response rate", color=RED)
    right.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=2))
    left.set_title("Complaint demand rose while response timeliness improved")
    left.set_xlabel("2024 reporting month")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "monthly_volume_and_risk.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    product = pd.read_csv(PROCESSED_DIR / "fact_product_monthly.csv")
    product = product.groupby("product", as_index=False)[["complaint_count", "timely_count", "untimely_count"]].sum()
    product["untimely_rate"] = product["untimely_count"] / (product["timely_count"] + product["untimely_count"])
    fig, ax = plt.subplots(figsize=(12, 7))
    sizes = 50 + 550 * np.sqrt(product["complaint_count"] / product["complaint_count"].max())
    ax.scatter(product["complaint_count"], product["untimely_rate"], s=sizes, color=TEAL, alpha=0.75, edgecolor="white")
    ax.set_xscale("log")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=1))
    ax.xaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
    ax.grid(True, which="major")
    ax.set_title("Product risk separates high-volume workload from high-rate exceptions")
    ax.set_xlabel("Complaint count (log scale)")
    ax.set_ylabel("Untimely response rate")
    label_rows = product.nlargest(6, "untimely_count")
    for row in label_rows.itertuples():
        ax.annotate(row.product, (row.complaint_count, row.untimely_rate), xytext=(6, 4), textcoords="offset points", fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "product_risk_matrix.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    issues = pd.read_csv(PROCESSED_DIR / "fact_issue_product.csv").nlargest(10, "untimely_count").sort_values("untimely_count")
    labels = issues["issue"].str.slice(0, 55)
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.barh(labels, issues["untimely_count"], color=ORANGE)
    ax.set_title("Top operational issue queues by untimely responses")
    ax.set_xlabel("Untimely responses")
    ax.xaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
    ax.grid(axis="x")
    for index, value in enumerate(issues["untimely_count"]):
        ax.text(value + 12, index, f"{value:,.0f}", va="center", fontsize=9, color=GRAY)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "issue_priority.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    company = pd.read_csv(PROCESSED_DIR / "fact_company_product.csv")
    company = company[company["complaint_count"] >= MIN_COMPANY_COMPLAINTS].copy()
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.scatter(company["complaint_count"], 1 - company["timely_rate"], s=28, color=BLUE, alpha=0.35)
    ax.set_xscale("log")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=0))
    ax.xaxis.set_major_formatter(mtick.StrMethodFormatter("{x:,.0f}"))
    ax.grid(True, which="major")
    ax.set_title("Company-product triage matrix (minimum 100 complaints)")
    ax.set_xlabel("Complaint count (log scale)")
    ax.set_ylabel("Untimely response rate")
    for row in company.nlargest(8, "untimely_count").itertuples():
        label = f"{row.company[:25]} / {row.product[:20]}"
        ax.annotate(label, (row.complaint_count, 1 - row.timely_rate), xytext=(5, 4), textcoords="offset points", fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "company_product_triage.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    print(f"Created figures in {FIGURES_DIR}")


if __name__ == "__main__":
    create()
