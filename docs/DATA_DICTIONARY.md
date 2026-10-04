# Data Dictionary

All published facts are aggregate. Counts are whole numbers and rates are decimal fractions.

## Shared metrics

| Field | Definition |
|---|---|
| complaint_count | Number of complaint records |
| timely_count | Records where `Timely response? = Yes` |
| untimely_count | Records where `Timely response? = No` |
| timely_rate | timely_count / (timely_count + untimely_count) |
| monetary_relief_count | Response category is closed with monetary relief |
| monetary_relief_rate | monetary_relief_count / complaint_count |
| nonmonetary_relief_count | Response category is closed with non-monetary relief |
| public_response_count | Nonblank company public response |
| public_response_rate | public_response_count / complaint_count |

## Tables

| File | Grain | Purpose |
|---|---|---|
| executive_kpis.csv | Reporting year | Headline scorecard |
| dim_date.csv | Month | Date labels, key, quarter |
| dim_product.csv | Product | Product dimension |
| dim_company.csv | Company | Company dimension |
| dim_issue.csv | Product + issue | Issue dimension |
| fact_monthly.csv | Month | Portfolio trend |
| fact_product_monthly.csv | Month + product | Product trends |
| fact_company_product.csv | Company + product | Triage and What-If analysis |
| fact_issue_product.csv | Product + issue | Root-cause prioritization |
| fact_company_monthly.csv | Month + company | Company trend |
| fact_channel_monthly.csv | Month + submission channel | Intake mix |
| fact_state.csv | State | Annual geographic workload |
| fact_response_annual.csv | Company response category | Response-outcome mix |
| data_quality_summary.csv | Quality check | Source validation evidence |

## Company-product extensions

| Field | Definition |
|---|---|
| company_comparison_eligible | TRUE when complaint_count ≥ 100 |
| priority_rank | Dense rank by untimely_count, descending |
| additional_timely_for_98pct | Minimum additional timely responses needed for 98% |
| additional_timely_for_99pct | Minimum additional timely responses needed for 99% |
| additional_timely_for_995pct | Minimum additional timely responses needed for 99.5% |
