-- Minimal SQLite-compatible schema for the core marts.
CREATE TABLE fact_monthly (
    month_key INTEGER PRIMARY KEY,
    month TEXT NOT NULL,
    complaint_count INTEGER NOT NULL,
    timely_count INTEGER NOT NULL,
    untimely_count INTEGER NOT NULL,
    monetary_relief_count INTEGER NOT NULL,
    nonmonetary_relief_count INTEGER NOT NULL,
    public_response_count INTEGER NOT NULL,
    timely_rate REAL,
    monetary_relief_rate REAL,
    nonmonetary_relief_rate REAL,
    public_response_rate REAL
);

CREATE TABLE fact_company_product (
    product_key INTEGER NOT NULL,
    company_key INTEGER NOT NULL,
    company TEXT NOT NULL,
    product TEXT NOT NULL,
    complaint_count INTEGER NOT NULL,
    timely_count INTEGER NOT NULL,
    untimely_count INTEGER NOT NULL,
    timely_rate REAL,
    company_comparison_eligible INTEGER NOT NULL,
    priority_rank INTEGER NOT NULL
);

CREATE INDEX idx_company_product_priority
ON fact_company_product (company_comparison_eligible, untimely_count DESC);
