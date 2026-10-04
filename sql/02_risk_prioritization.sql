-- Company-product queues with both sufficient volume and elevated exception count
SELECT
    company,
    product,
    complaint_count,
    untimely_count,
    ROUND(100.0 * timely_rate, 2) AS timely_rate_pct,
    priority_rank
FROM fact_company_product
WHERE company_comparison_eligible = 1
ORDER BY untimely_count DESC, complaint_count DESC
LIMIT 20;

-- Transparent 99% target scenario in SQL
SELECT
    company,
    product,
    complaint_count,
    timely_count,
    untimely_count,
    MAX(
        0,
        CAST(((timely_count + untimely_count) * 0.99) + 0.999999 AS INTEGER) - timely_count
    ) AS additional_timely_needed_for_99pct
FROM fact_company_product
WHERE company_comparison_eligible = 1
ORDER BY additional_timely_needed_for_99pct DESC, complaint_count DESC
LIMIT 20;
