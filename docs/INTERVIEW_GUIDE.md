# Interview Guide

## 60-second version

“ComplaintLens is an operational-risk analytics project built on 2.73 million official CFPB complaints from 2024. I chose a fixed post-taxonomy window, processed the 5.4 GB source in chunks, built aggregate marts and a Power BI semantic model, and added automated reconciliation and quality checks. The headline timely-response rate was 99.72%, but segmentation revealed concentrated exceptions in debt collection, student loans, and a small number of company-product queues. The dashboard includes a What-If service target so an operations lead can quantify the improvement gap instead of only viewing historical KPIs.”

## Questions to expect

**Why not rank companies by complaint count?**
Counts are exposure-sensitive and the CFPB data is not representative. I use count as workload, show timeliness with its denominator, and require at least 100 complaints for company-product comparisons.

**Why 2024?**
It is a closed year after the August 2023 taxonomy change. That improves comparability and avoids a partial-year denominator.

**Why aggregate before Power BI?**
The raw CSV is 5.4 GB uncompressed. The business questions do not require record-level narratives, so aggregated marts improve refresh speed, privacy posture, and repository usability.

**What is the most important finding?**
The portfolio average is excellent but not operationally sufficient. A small number of issue and company-product queues account for a large share of exceptions, so targeted remediation is more appropriate than a portfolio-wide response.

**What would you add internally?**
Staffing hours, queue age, escalation stage, ownership, customer/product exposure, SLA timestamps, and root-cause codes. Those fields would support capacity forecasting and causal diagnosis.

**Is the target-gap analysis predictive?**
No. It is a transparent scenario calculation under a fixed denominator.

## STAR framing

- **Situation:** aggregate service levels obscured pockets of complaint-response risk.
- **Task:** build a reproducible system to prioritize investigation.
- **Action:** designed KPI contracts, chunked ETL, dimensional marts, QA controls, SQL analysis, and a Power BI What-If experience.
- **Result:** reduced 18 million scanned public rows to a compact 2.4 MB decision layer and isolated the queues driving 7,737 untimely responses.
