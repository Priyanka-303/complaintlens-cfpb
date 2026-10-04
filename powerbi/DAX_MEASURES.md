# DAX Measures

Create an empty `_Measures` table and place these measures there.

## Portfolio measures

```DAX
Portfolio Complaints =
SUM ( fact_monthly[complaint_count] )

Portfolio Timely Responses =
SUM ( fact_monthly[timely_count] )

Portfolio Untimely Responses =
SUM ( fact_monthly[untimely_count] )

Portfolio Valid Responses =
[Portfolio Timely Responses] + [Portfolio Untimely Responses]

Portfolio Timely Rate =
DIVIDE ( [Portfolio Timely Responses], [Portfolio Valid Responses] )

Portfolio Untimely Rate =
1 - [Portfolio Timely Rate]

Portfolio Monetary Relief =
SUM ( fact_monthly[monetary_relief_count] )

Portfolio Monetary Relief Rate =
DIVIDE ( [Portfolio Monetary Relief], [Portfolio Complaints] )

Complaint MoM % =
VAR PreviousMonth =
    CALCULATE ( [Portfolio Complaints], DATEADD ( dim_date[month_start], -1, MONTH ) )
RETURN
    DIVIDE ( [Portfolio Complaints] - PreviousMonth, PreviousMonth )
```

## Company-product queue measures

```DAX
Queue Complaints =
SUM ( fact_company_product[complaint_count] )

Queue Timely Responses =
SUM ( fact_company_product[timely_count] )

Queue Untimely Responses =
SUM ( fact_company_product[untimely_count] )

Queue Valid Responses =
[Queue Timely Responses] + [Queue Untimely Responses]

Queue Timely Rate =
DIVIDE ( [Queue Timely Responses], [Queue Valid Responses] )

Queue Untimely Rate =
1 - [Queue Timely Rate]

Queue Share of Untimely =
DIVIDE (
    [Queue Untimely Responses],
    CALCULATE ( [Queue Untimely Responses], ALLSELECTED ( dim_company ), ALLSELECTED ( dim_product ) )
)

Eligible Queue =
IF ( [Queue Complaints] >= 100, 1, 0 )
```

Apply `Eligible Queue = 1` as a visual filter on company comparisons.

## What-If target

Create this calculated table. Do **not** add a relationship.

```DAX
Target Timely Rate =
GENERATESERIES ( 0.980, 1.000, 0.001 )

Selected Target Timely Rate =
SELECTEDVALUE ( 'Target Timely Rate'[Value], 0.990 )

Additional Timely Needed =
VAR RequiredTimely =
    CEILING ( [Queue Valid Responses] * [Selected Target Timely Rate], 1 )
RETURN
    MAX ( 0, RequiredTimely - [Queue Timely Responses] )

Target Gap (pp) =
MAX ( 0, [Selected Target Timely Rate] - [Queue Timely Rate] )

Target Status =
IF ( [Queue Timely Rate] >= [Selected Target Timely Rate], "At/above target", "Below target" )
```

Format the target value and gap as percentages. Put `Target Timely Rate[Value]` on a single-select slider from 98.0% to 100.0%.

## Issue measures

```DAX
Issue Complaints =
SUM ( fact_issue_product[complaint_count] )

Issue Untimely Responses =
SUM ( fact_issue_product[untimely_count] )

Issue Timely Rate =
DIVIDE (
    SUM ( fact_issue_product[timely_count] ),
    SUM ( fact_issue_product[timely_count] ) + SUM ( fact_issue_product[untimely_count] )
)
```
