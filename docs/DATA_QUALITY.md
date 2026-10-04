# Data Quality Report

## 2024 validation result

| Check | Result |
|---|---:|
| In-scope rows | 2,734,269 |
| Unique Complaint IDs | 2,734,269 |
| Duplicate Complaint IDs | 0 |
| Missing complaint ID | 0 |
| Missing company | 0 |
| Missing product | 0 |
| Missing issue | 6 |
| Missing state | 5,999 (0.22%) |
| Missing timeliness | 0 |
| Invalid timeliness | 0 |
| Date sent before received | 0 |

## Treatment

- Missing state is retained as `Unknown`; rows remain in all non-geographic metrics.
- Six missing issues remain in product totals and are excluded only from meaningful issue labels.
- No imputation is performed.
- Duplicate IDs would be reported as a pipeline failure candidate; none were found.

## Automated controls

`src/validate_data.py` checks monthly completeness, annual reconciliation, rate ranges, negative values, surrogate keys, and dimension-key uniqueness. Python's standard `unittest` framework covers metric formula behavior, and GitHub Actions runs both on every push and pull request.
