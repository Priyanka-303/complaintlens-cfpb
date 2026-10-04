# Methodology

## Analytical window

- Complaint received date: 2024-01-01 through 2024-12-31
- Source snapshot: 2026-09-27
- Grain of raw source: one row per Complaint ID
- Grain of published facts: documented in `DATA_DICTIONARY.md`

A closed 2024 window was selected because CFPB product and issue options changed in August 2023. This avoids comparing incompatible pre/post taxonomy periods and prevents a partial current-year view.

## Pipeline

1. Download the official compressed CSV.
2. Read only required columns in 250,000-row chunks.
3. Filter on `Date received` rather than response date.
4. Normalize blanks and derive binary metric flags.
5. Aggregate into monthly, product, issue, company-product, state, channel, and response marts.
6. Create stable surrogate keys and dimensions.
7. Reconcile totals, validate rates and keys, then generate figures.

## Metric logic

`Timely response rate = Timely responses / (Timely responses + Untimely responses)`

The denominator excludes blank/invalid timeliness values. In the 2024 slice there were none.

`Target improvement gap = max(0, ceil(Valid responses × Selected target) − Timely responses)`

This is a scenario measure, not a forecast. It expresses the minimum count of responses that would need to move from untimely to timely under a fixed denominator.

## Comparison rules

- Company-product comparisons are eligible at 100 or more complaints.
- Counts and rates are displayed together.
- Untimely count is the default triage ranking because it combines operational scale and exception volume without inventing a weighted score.
- Geography is descriptive only; no population normalization is available in the project.

## Known limitations

- Complaints are not representative of all consumer experiences.
- Company market share, customer count, and product exposure are unavailable.
- Complaint narratives are intentionally excluded.
- A later CFPB snapshot may contain backfills or corrections.
- `Company response to consumer = Untimely response` is a response category and is not identical to `Timely response? = No`; the timeliness flag is authoritative for the KPI.
