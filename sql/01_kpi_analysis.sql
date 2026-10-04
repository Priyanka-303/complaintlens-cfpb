-- 1. Portfolio KPI reconciliation
SELECT
    SUM(complaint_count) AS complaints,
    SUM(timely_count) AS timely_responses,
    SUM(untimely_count) AS untimely_responses,
    1.0 * SUM(timely_count) / NULLIF(SUM(timely_count) + SUM(untimely_count), 0) AS timely_rate
FROM fact_monthly;

-- 2. Monthly demand and response risk
SELECT
    month,
    complaint_count,
    untimely_count,
    1.0 * untimely_count / NULLIF(timely_count + untimely_count, 0) AS untimely_rate
FROM fact_monthly
ORDER BY month_key;

-- 3. Month-over-month complaint change
WITH trend AS (
    SELECT
        month,
        complaint_count,
        LAG(complaint_count) OVER (ORDER BY month_key) AS previous_month
    FROM fact_monthly
)
SELECT
    month,
    complaint_count,
    ROUND(100.0 * (complaint_count - previous_month) / NULLIF(previous_month, 0), 2) AS complaint_mom_pct
FROM trend;
