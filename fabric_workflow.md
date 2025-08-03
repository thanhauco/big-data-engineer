# Fabric Workflow Notes

## OneLake / Lakehouse Pattern

This repository models a Microsoft Fabric workflow that follows a common lakehouse pattern for business reporting:

1. Raw source files land in ADLS and are processed through Spark.
2. Cleaned data is written to a Delta-formatted curated path in the data lake.
3. The curated data is registered as a table in Microsoft Fabric OneLake.
4. A semantic layer or SQL view exposes business metrics to downstream reporting.
5. Kusto and dashboard alerts monitor freshness, quality, and saturation.

## Example Notebook Logic

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("FabricGoldRefresh").getOrCreate()

df = spark.read.format("delta").load("abfss://curated@contosodata.dfs.core.windows.net/gold/sales")
df.createOrReplaceTempView("gold_sales")

result = spark.sql("""
    SELECT region, SUM(amount) AS total_revenue
    FROM gold_sales
    GROUP BY region
""")

result.show()
```

## Operational Considerations

- Validate Delta table freshness before publishing to reporting consumers.
- Use partitioning on date and business keys to reduce scan volume.
- Monitor row count drift and null saturation in Fabric or Kusto.
- Keep curated business views small and stable for analyst consumption.
