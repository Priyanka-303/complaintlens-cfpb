# Dashboard Specification

Canvas: 16:9. Theme: `ComplaintLens_Theme.json`. Use a white background, navy titles, blue primary series, teal positive status, and orange/red exceptions.

## Page 1 — Executive overview

**Question:** Is demand or response risk changing?

- Top row cards: Portfolio Complaints, Portfolio Timely Rate, Portfolio Untimely Responses, Portfolio Monetary Relief Rate
- Main visual: combo chart by month—complaint count as columns and untimely rate as a line
- Product view: horizontal bar chart for complaint volume with untimely rate in tooltip
- Response view: 100% stacked bar from `fact_response_annual`
- Slicers: month and product
- Annotation: “Volume is workload, not market-adjusted performance.”

## Page 2 — Risk triage

**Question:** Which queues should operations investigate first?

- Scatter: complaint count (log X), untimely rate (Y), untimely count (size), product (legend), company (details)
- Visual filter: Eligible Queue = 1
- Ranked table: company, product, complaints, untimely, timely rate, share of untimely
- Issue bar: top 10 issues by untimely responses
- Slicers: product and company
- Conditional formatting: timely rate red below 98%, amber 98%–99%, green at/above 99%

## Page 3 — Target scenario

**Question:** What improvement is needed to reach the selected service target?

- Single-select target slider: 98.0% to 100.0%
- Cards: Selected Target, Queue Timely Rate, Target Gap, Additional Timely Needed
- Decomposition tree: Additional Timely Needed → product → company
- Table: eligible company-product queues below target, sorted by Additional Timely Needed
- Button/bookmark: reset target to 99.0%
- Disclaimer: “Scenario assumes a fixed response denominator; it is not a forecast.”

## Page 4 — Data quality and methodology

- Cards: source rows scanned, in-scope rows, duplicate IDs, missing state
- Table: all quality checks and values
- Text: source URL, snapshot date, reporting window, comparison threshold
- Navigation links to BRD, methodology, and repository README

## Interaction rules

- Product slicers may filter product, issue, and company-product visuals.
- Company slicers do not affect portfolio monthly facts; keep them off the executive page.
- Turn off cross-highlighting when it produces a misleading cross-grain comparison.
- Always include denominator counts in tooltips for rates.
