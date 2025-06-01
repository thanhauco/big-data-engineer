from __future__ import annotations

from big_data_engineer.azure_pipeline import build_end_to_end_pipeline_summary
from big_data_engineer.config import SparkJobConfig
from big_data_engineer.spark_jobs import build_daily_revenue_summary


def main() -> None:
    config = SparkJobConfig(
        app_name="BigDataEngineerDemo",
        source_path="data/sample_telemetry.csv",
        output_path="data/output/gold_sales",
        partitions=4,
        business_date="2026-09-14",
    )

    raw_records = [
        {"event_id": "evt-1001", "customer_id": "cust-01", "order_id": "ord-901", "amount": 120.5, "region": "West"},
        {"event_id": "evt-1002", "customer_id": "cust-02", "order_id": "ord-902", "amount": 85.0, "region": "East"},
        {"event_id": "evt-1003", "customer_id": "cust-01", "order_id": "ord-903", "amount": 210.75, "region": "West"},
        {"event_id": "evt-1004", "customer_id": "cust-03", "order_id": "ord-904", "amount": 0.0, "region": "Central"},
    ]

    bronze_summary = build_end_to_end_pipeline_summary(raw_records)
    daily_summary = build_daily_revenue_summary(raw_records, partition_col=config.partition_by)

    print(f"Spark app: {config.app_name}")
    print(f"Bronze -> Gold pipeline summary: {bronze_summary}")
    print(f"Partition: {config.partition_by}")
    print(f"Daily business summary: {daily_summary}")


if __name__ == "__main__":
    main()
