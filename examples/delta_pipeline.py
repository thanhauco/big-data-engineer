from __future__ import annotations

from big_data_engineer.delta_pipeline import write_delta_gold_table


def main() -> None:
    records = [
        {
            "event_id": "evt-1001",
            "customer_id": "cust-01",
            "order_id": "ord-901",
            "event_ts": "2026-09-14T08:01:00Z",
            "amount": 120.5,
            "region": "West",
            "date_partition": "2026-09-14",
        },
        {
            "event_id": "evt-1002",
            "customer_id": "cust-02",
            "order_id": "ord-902",
            "event_ts": "2026-09-14T09:15:00Z",
            "amount": 85.0,
            "region": "East",
            "date_partition": "2026-09-14",
        },
        {
            "event_id": "evt-1003",
            "customer_id": "cust-01",
            "order_id": "ord-903",
            "event_ts": "2026-09-14T10:45:00Z",
            "amount": 210.75,
            "region": "West",
            "date_partition": "2026-09-14",
        },
    ]

    result = write_delta_gold_table(
        records=records,
        output_path="data/output/gold_sales_delta",
        table_name="gold_sales",
        partition_col="date_partition",
        mode="overwrite",
    )
    print(result)


if __name__ == "__main__":
    main()
