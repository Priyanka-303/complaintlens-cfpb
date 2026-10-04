"""Create compact analytical marts from the official CFPB bulk CSV.

The raw file is intentionally excluded from Git. This pipeline scans the source
in chunks and publishes only aggregated, Power BI-ready CSVs for a fixed year.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from datetime import date
from pathlib import Path

import pandas as pd

try:
    from .config import MIN_COMPANY_COMPLAINTS, PROCESSED_DIR, REPORTING_YEAR, SOURCE_FILE
except ImportError:  # Direct script execution
    from config import MIN_COMPANY_COMPLAINTS, PROCESSED_DIR, REPORTING_YEAR, SOURCE_FILE


SOURCE_COLUMNS = [
    "Date received",
    "Product",
    "Issue",
    "Company public response",
    "Company",
    "State",
    "Submitted via",
    "Date sent to company",
    "Company response to consumer",
    "Timely response?",
    "Complaint ID",
]

METRICS = [
    "complaint_count",
    "timely_count",
    "untimely_count",
    "monetary_relief_count",
    "nonmonetary_relief_count",
    "public_response_count",
]


def _blank_metrics() -> list[int]:
    return [0] * len(METRICS)


def _merge_group(target: dict, grouped: pd.DataFrame) -> None:
    for index, values in grouped.iterrows():
        key = index if isinstance(index, tuple) else (index,)
        bucket = target[key]
        for position, metric in enumerate(METRICS):
            bucket[position] += int(values[metric])


def _aggregate_chunk(frame: pd.DataFrame, keys: list[str], target: dict) -> None:
    grouped = frame.groupby(keys, dropna=False, observed=True)[METRICS].sum()
    _merge_group(target, grouped)


def _to_frame(accumulator: dict, keys: list[str]) -> pd.DataFrame:
    records = []
    for key, values in accumulator.items():
        record = dict(zip(keys, key))
        record.update(dict(zip(METRICS, values)))
        records.append(record)
    result = pd.DataFrame(records)
    if result.empty:
        return result

    valid = result["timely_count"] + result["untimely_count"]
    result["timely_rate"] = (result["timely_count"] / valid.where(valid > 0)).round(6)
    result["monetary_relief_rate"] = (
        result["monetary_relief_count"] / result["complaint_count"].where(result["complaint_count"] > 0)
    ).round(6)
    result["nonmonetary_relief_rate"] = (
        result["nonmonetary_relief_count"] / result["complaint_count"].where(result["complaint_count"] > 0)
    ).round(6)
    result["public_response_rate"] = (
        result["public_response_count"] / result["complaint_count"].where(result["complaint_count"] > 0)
    ).round(6)
    return result


def _write(frame: pd.DataFrame, name: str, sort_by: list[str] | None = None) -> None:
    if sort_by:
        frame = frame.sort_values(sort_by, kind="stable")
    frame.to_csv(PROCESSED_DIR / name, index=False)


def build(source: Path = SOURCE_FILE, year: int = REPORTING_YEAR) -> dict:
    if not source.exists():
        raise FileNotFoundError(f"Raw source not found: {source}. Run download_data.py first.")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    accumulators = {
        "month": defaultdict(_blank_metrics),
        "product_month": defaultdict(_blank_metrics),
        "company_product": defaultdict(_blank_metrics),
        "issue_product": defaultdict(_blank_metrics),
        "state": defaultdict(_blank_metrics),
        "channel_month": defaultdict(_blank_metrics),
        "response": defaultdict(_blank_metrics),
        "company_month": defaultdict(_blank_metrics),
    }
    seen_ids: set[str] = set()
    quality = defaultdict(int)
    year_prefix = f"{year}-"

    reader = pd.read_csv(
        source,
        compression="zip",
        usecols=SOURCE_COLUMNS,
        dtype="string",
        chunksize=250_000,
        keep_default_na=False,
    )
    for chunk_number, chunk in enumerate(reader, start=1):
        quality["source_rows_scanned"] += len(chunk)
        frame = chunk[chunk["Date received"].str.startswith(year_prefix, na=False)].copy()
        if frame.empty:
            continue

        frame.columns = [
            "date_received",
            "product",
            "issue",
            "company_public_response",
            "company",
            "state",
            "submitted_via",
            "date_sent_to_company",
            "company_response",
            "timely_response",
            "complaint_id",
        ]
        for column in frame.columns:
            frame[column] = frame[column].fillna("").astype("string").str.strip()

        quality["in_scope_rows"] += len(frame)
        ids = frame["complaint_id"].tolist()
        quality["duplicate_complaint_ids"] += sum(identifier in seen_ids for identifier in ids)
        seen_ids.update(ids)
        quality["missing_complaint_id"] += int((frame["complaint_id"] == "").sum())
        quality["missing_product"] += int((frame["product"] == "").sum())
        quality["missing_issue"] += int((frame["issue"] == "").sum())
        quality["missing_company"] += int((frame["company"] == "").sum())
        quality["missing_state"] += int((frame["state"] == "").sum())
        quality["invalid_timely_response"] += int(
            (~frame["timely_response"].isin(["Yes", "No", ""])).sum()
        )
        quality["missing_timely_response"] += int((frame["timely_response"] == "").sum())
        quality["date_sent_before_received"] += int(
            (
                (frame["date_sent_to_company"] != "")
                & (frame["date_sent_to_company"] < frame["date_received"])
            ).sum()
        )

        frame["month"] = frame["date_received"].str.slice(0, 7)
        frame["state"] = frame["state"].replace("", "Unknown")
        frame["submitted_via"] = frame["submitted_via"].replace("", "Unknown")
        frame["company_response"] = frame["company_response"].replace("", "Unknown")
        frame["complaint_count"] = 1
        frame["timely_count"] = frame["timely_response"].eq("Yes").astype("int8")
        frame["untimely_count"] = frame["timely_response"].eq("No").astype("int8")
        frame["monetary_relief_count"] = frame["company_response"].eq(
            "Closed with monetary relief"
        ).astype("int8")
        frame["nonmonetary_relief_count"] = frame["company_response"].eq(
            "Closed with non-monetary relief"
        ).astype("int8")
        frame["public_response_count"] = frame["company_public_response"].ne("").astype("int8")

        _aggregate_chunk(frame, ["month"], accumulators["month"])
        _aggregate_chunk(frame, ["month", "product"], accumulators["product_month"])
        _aggregate_chunk(frame, ["company", "product"], accumulators["company_product"])
        _aggregate_chunk(frame, ["product", "issue"], accumulators["issue_product"])
        _aggregate_chunk(frame, ["state"], accumulators["state"])
        _aggregate_chunk(frame, ["month", "submitted_via"], accumulators["channel_month"])
        _aggregate_chunk(frame, ["company_response"], accumulators["response"])
        _aggregate_chunk(frame, ["month", "company"], accumulators["company_month"])
        print(f"Processed chunk {chunk_number}; in-scope rows: {quality['in_scope_rows']:,}")

    month = _to_frame(accumulators["month"], ["month"])
    product_month = _to_frame(accumulators["product_month"], ["month", "product"])
    company_product = _to_frame(accumulators["company_product"], ["company", "product"])
    issue_product = _to_frame(accumulators["issue_product"], ["product", "issue"])
    state = _to_frame(accumulators["state"], ["state"])
    channel_month = _to_frame(accumulators["channel_month"], ["month", "submitted_via"])
    response = _to_frame(accumulators["response"], ["company_response"])
    company_month = _to_frame(accumulators["company_month"], ["month", "company"])

    date_dim = pd.DataFrame({"month": sorted(month["month"].unique())})
    date_dim["month_key"] = date_dim["month"].str.replace("-", "").astype(int)
    date_dim["month_start"] = date_dim["month"] + "-01"
    date_dim["month_label"] = pd.to_datetime(date_dim["month_start"]).dt.strftime("%b %Y")
    date_dim["quarter"] = "Q" + (((date_dim["month_key"] % 100 - 1) // 3) + 1).astype(str)

    product_dim = pd.DataFrame({"product": sorted(product_month["product"].unique())})
    product_dim.insert(0, "product_key", range(1, len(product_dim) + 1))
    company_dim = pd.DataFrame({"company": sorted(company_product["company"].unique())})
    company_dim.insert(0, "company_key", range(1, len(company_dim) + 1))
    issue_dim = issue_product[["product", "issue"]].drop_duplicates().sort_values(["product", "issue"])
    issue_dim.insert(0, "issue_key", range(1, len(issue_dim) + 1))

    product_map = dict(zip(product_dim["product"], product_dim["product_key"]))
    company_map = dict(zip(company_dim["company"], company_dim["company_key"]))
    month_map = dict(zip(date_dim["month"], date_dim["month_key"]))
    issue_map = {(row.product, row.issue): row.issue_key for row in issue_dim.itertuples()}

    for frame in [product_month, company_product, issue_product]:
        frame.insert(0, "product_key", frame["product"].map(product_map))
    for frame in [company_product, company_month]:
        frame.insert(0, "company_key", frame["company"].map(company_map))
    for frame in [month, product_month, channel_month, company_month]:
        frame.insert(0, "month_key", frame["month"].map(month_map))
    issue_product.insert(
        0,
        "issue_key",
        [issue_map[(product, issue)] for product, issue in zip(issue_product["product"], issue_product["issue"])],
    )

    company_product["company_comparison_eligible"] = company_product["complaint_count"].ge(
        MIN_COMPANY_COMPLAINTS
    )
    company_product["priority_rank"] = (
        company_product["untimely_count"].rank(method="dense", ascending=False).astype(int)
    )
    valid_responses = company_product["timely_count"] + company_product["untimely_count"]
    for target in [0.98, 0.99, 0.995]:
        label = str(target).replace("0.", "")
        company_product[f"additional_timely_for_{label}pct"] = (
            (valid_responses * target).apply(math.ceil) - company_product["timely_count"]
        ).clip(lower=0)

    annual = month[METRICS].sum()
    valid_annual = int(annual["timely_count"] + annual["untimely_count"])
    executive_kpis = pd.DataFrame(
        [
            {
                "reporting_year": year,
                **{metric: int(annual[metric]) for metric in METRICS},
                "timely_rate": round(int(annual["timely_count"]) / valid_annual, 6) if valid_annual else None,
                "monetary_relief_rate": round(int(annual["monetary_relief_count"]) / int(annual["complaint_count"]), 6),
                "public_response_rate": round(int(annual["public_response_count"]) / int(annual["complaint_count"]), 6),
                "source_snapshot_date": date.today().isoformat(),
            }
        ]
    )

    _write(date_dim, "dim_date.csv", ["month_key"])
    _write(product_dim, "dim_product.csv", ["product_key"])
    _write(company_dim, "dim_company.csv", ["company_key"])
    _write(issue_dim, "dim_issue.csv", ["issue_key"])
    _write(month, "fact_monthly.csv", ["month_key"])
    _write(product_month, "fact_product_monthly.csv", ["month_key", "complaint_count"])
    _write(company_product, "fact_company_product.csv", ["priority_rank", "company", "product"])
    _write(issue_product, "fact_issue_product.csv", ["untimely_count", "complaint_count"])
    _write(state, "fact_state.csv", ["complaint_count"])
    _write(channel_month, "fact_channel_monthly.csv", ["month_key", "complaint_count"])
    _write(response, "fact_response_annual.csv", ["complaint_count"])
    _write(company_month, "fact_company_monthly.csv", ["month_key", "complaint_count"])
    _write(executive_kpis, "executive_kpis.csv")

    quality["unique_complaint_ids"] = len(seen_ids)
    quality_frame = pd.DataFrame(
        [{"check": key, "value": int(value)} for key, value in sorted(quality.items())]
    )
    _write(quality_frame, "data_quality_summary.csv", ["check"])

    manifest = {
        "project": "ComplaintLens",
        "reporting_year": year,
        "source": "CFPB Consumer Complaint Database",
        "source_url": "https://files.consumerfinance.gov/ccdb/complaints.csv.zip",
        "source_snapshot_date": date.today().isoformat(),
        "in_scope_rows": int(quality["in_scope_rows"]),
        "minimum_company_complaints_for_comparison": MIN_COMPANY_COMPLAINTS,
        "published_files": sorted(path.name for path in PROCESSED_DIR.glob("*.csv")),
    }
    (PROCESSED_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE_FILE)
    parser.add_argument("--year", type=int, default=REPORTING_YEAR)
    arguments = parser.parse_args()
    build(arguments.source, arguments.year)
