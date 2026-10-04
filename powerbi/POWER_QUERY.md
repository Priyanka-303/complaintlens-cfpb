# Power Query Setup

Create a text parameter named `ProjectRoot` pointing to the cloned `ComplaintLens` folder. Use the function below to import each processed CSV.

```powerquery
(FileName as text) as table =>
let
    Source = Csv.Document(
        File.Contents(ProjectRoot & "\\data\\processed\\" & FileName),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars = true])
in
    Headers
```

Example query:

```powerquery
let
    Source = LoadProcessedCsv("fact_monthly.csv"),
    Types = Table.TransformColumnTypes(
        Source,
        {
            {"month_key", Int64.Type},
            {"month", type text},
            {"complaint_count", Int64.Type},
            {"timely_count", Int64.Type},
            {"untimely_count", Int64.Type},
            {"timely_rate", Percentage.Type}
        }
    )
in
    Types
```

Set all count columns to Whole Number, key columns to Whole Number, date fields to Date, eligibility to True/False, and rates to Decimal Number before applying percentage formatting in the model.
