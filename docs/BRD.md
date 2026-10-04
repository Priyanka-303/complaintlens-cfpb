# Business Requirements Document

## 1. Business problem

A consumer-finance complaint operations team needs a repeatable way to identify response-risk concentrations. A portfolio-wide timely-response rate can appear healthy while specific products, issues, or company-product queues generate a disproportionate number of exceptions.

## 2. Decision and users

**Primary decision:** where should operations leaders investigate capacity, workflow, or escalation controls first?

| User | Need | Decision cadence |
|---|---|---|
| Head of complaint operations | Portfolio performance and exceptions | Monthly |
| Product operations lead | Product and issue backlog priorities | Weekly/monthly |
| Compliance analyst | Timeliness and response-outcome monitoring | Monthly |
| BI analyst | Traceable definitions and reusable model | On refresh |

## 3. Objectives

1. Quantify complaint workload, timely responses, untimely responses, response outcomes, and public-response coverage.
2. Reveal trends by month and concentrations by product, issue, company-product, channel, and state.
3. Separate high-volume workload from high-rate response risk.
4. Let users test target timely-response rates and quantify the improvement gap.
5. Make every published KPI reproducible and reconciled to the source.

## 4. Scope

**In scope:** complaints received from 2024-01-01 through 2024-12-31; public structured fields; aggregate operational analytics; Power BI-ready marts.

**Out of scope:** complaint narratives; prediction of individual complaints; causal claims; market-share-adjusted company rankings; population-adjusted geography; legal conclusions; live alerting.

## 5. KPI requirements

| KPI | Definition | Acceptance rule |
|---|---|---|
| Complaint count | Count of unique Complaint IDs received in 2024 | Reconciles across month and product-month facts |
| Timely response rate | Timely / (Timely + Untimely) | Between 0% and 100%; denominator visible |
| Untimely count | Timely response? = No | Reconciles to executive total |
| Monetary relief rate | Closed with monetary relief / complaints | Between 0% and 100% |
| Public response rate | Nonblank company public response / complaints | Between 0% and 100% |
| Target improvement gap | max(0, ceil(valid responses × target) − timely responses) | Responds to Power BI filter context |

## 6. Functional requirements

- Filter by month, product, issue, company, channel, state, and response category where supported by each fact table.
- Display volume and timeliness together.
- Apply a minimum 100-complaint threshold to company-product comparisons.
- Provide executive overview, operational drilldown, and What-If pages.
- Refresh from the official bulk file without manual edits.
- Retain a snapshot date and fixed reporting window.

## 7. Non-functional requirements

- Reproducible on Python 3.11+
- Raw file excluded from Git; processed deliverables small enough for normal clone/pull
- Automated unit, reconciliation, range, uniqueness, and key checks
- Metric logic documented in code and prose
- No personal complaint narrative data stored in the repository

## 8. Acceptance criteria

- [x] 12 monthly periods present
- [x] Monthly and product totals reconcile to 2,734,269 complaints
- [x] Zero duplicate in-scope Complaint IDs
- [x] Zero invalid timeliness values
- [x] All rates fall in [0, 1]
- [x] Power BI relationships and DAX documented
- [x] What-If target analysis implemented
- [x] Findings include limitations and avoid unsupported performance claims

## 9. Risks and controls

| Risk | Control |
|---|---|
| Complaint data is not representative | Label volume as workload; avoid market-quality ranking |
| Company exposure is unknown | Show counts and rates; apply minimum denominator |
| Taxonomy changed historically | Use a closed 2024 window after the August 2023 taxonomy change |
| Source can receive backfills | Record extraction date and keep window fixed |
| Small segments create volatile rates | Threshold company-product comparisons at 100 complaints |
