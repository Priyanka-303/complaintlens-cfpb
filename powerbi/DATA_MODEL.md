# Power BI Data Model

Use Import mode. Load all CSVs from `data/processed/` except the quality summary if you do not plan to build the QA page.

## Relationships

| From (1) | Key | To (*) | Key | Direction |
|---|---|---|---|---|
| dim_date | month_key | fact_monthly | month_key | Single |
| dim_date | month_key | fact_product_monthly | month_key | Single |
| dim_date | month_key | fact_company_monthly | month_key | Single |
| dim_date | month_key | fact_channel_monthly | month_key | Single |
| dim_product | product_key | fact_product_monthly | product_key | Single |
| dim_product | product_key | fact_company_product | product_key | Single |
| dim_product | product_key | fact_issue_product | product_key | Single |
| dim_company | company_key | fact_company_product | company_key | Single |
| dim_company | company_key | fact_company_monthly | company_key | Single |
| dim_issue | issue_key | fact_issue_product | issue_key | Single |

Do not relate fact tables to one another. `fact_state`, `fact_response_annual`, and `data_quality_summary` are intentionally standalone aggregate tables.

## Model conventions

- Mark `dim_date[month_start]` as a date and sort `month_label` by `month_key`.
- Hide surrogate keys from report view.
- Format rate fields as percentages with two decimals.
- Format counts with thousands separators and no decimals.
- Disable Auto date/time.
- Place all DAX measures in a dedicated empty `_Measures` table.
- Keep cross-filter direction single to prevent ambiguous paths.

## Grain warning

Each fact answers a different question. Do not add measures from unrelated fact tables to the same visual unless the dimensions and aggregation level are compatible. Portfolio trend measures use `fact_monthly`; triage and What-If measures use `fact_company_product`.
