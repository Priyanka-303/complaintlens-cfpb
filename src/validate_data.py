"""Fail-fast validation for published ComplaintLens marts."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

try:
    from .config import PROCESSED_DIR, REPORTING_YEAR
except ImportError:  # Direct script execution
    from config import PROCESSED_DIR, REPORTING_YEAR


def validate(data_dir: Path = PROCESSED_DIR) -> list[str]:
    errors: list[str] = []
    monthly = pd.read_csv(data_dir / "fact_monthly.csv")
    kpis = pd.read_csv(data_dir / "executive_kpis.csv").iloc[0]
    company = pd.read_csv(data_dir / "fact_company_product.csv")
    product = pd.read_csv(data_dir / "fact_product_monthly.csv")
    date_dim = pd.read_csv(data_dir / "dim_date.csv")

    if len(monthly) != 12:
        errors.append(f"Expected 12 monthly rows; found {len(monthly)}")
    if int(kpis["reporting_year"]) != REPORTING_YEAR:
        errors.append("Executive KPI reporting year does not match configuration")
    if int(monthly["complaint_count"].sum()) != int(kpis["complaint_count"]):
        errors.append("Monthly complaint count does not reconcile to executive KPI")
    if int(monthly["untimely_count"].sum()) != int(kpis["untimely_count"]):
        errors.append("Monthly untimely count does not reconcile to executive KPI")
    if int(product["complaint_count"].sum()) != int(kpis["complaint_count"]):
        errors.append("Product-month complaint count does not reconcile to executive KPI")
    if not monthly["timely_rate"].between(0, 1).all():
        errors.append("Monthly timely rate is outside [0, 1]")
    if (company[["complaint_count", "timely_count", "untimely_count"]].lt(0)).any().any():
        errors.append("Negative company-product counts detected")
    if company["company_key"].isna().any() or company["product_key"].isna().any():
        errors.append("Missing surrogate key in company-product fact")
    if date_dim["month_key"].duplicated().any():
        errors.append("Duplicate month key in date dimension")

    result = {"status": "PASS" if not errors else "FAIL", "checks_failed": errors}
    (data_dir / "validation_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    if errors:
        raise AssertionError("; ".join(errors))
    print("Validation PASS: all reconciliation, range, key, and grain checks succeeded.")
    return errors


if __name__ == "__main__":
    validate()
