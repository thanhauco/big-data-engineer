from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class FabricLakehouseTable:
    table_name: str
    schema: List[str]
    location: str = "/Tables"

    def as_sql(self) -> str:
        col_defs = ",\n  ".join(f"{col} STRING" for col in self.schema)
        return (
            f"CREATE TABLE {self.table_name} (\n  {col_defs}\n)\n"
            f"USING DELTA\nLOCATION '{self.location}/{self.table_name}'"
        )


def build_fabric_gold_table() -> FabricLakehouseTable:
    columns = ["event_id", "customer_id", "order_id", "event_ts", "amount", "region", "date_partition"]
    return FabricLakehouseTable(table_name="gold_orders", schema=columns, location="abfss://curated@contosodata.dfs.core.windows.net/gold")


def build_fabric_dashboard_metrics() -> Dict[str, float]:
    return {
        "total_revenue": 256789.42,
        "avg_order_value": 214.25,
        "orders_processed": 1197,
        "p95_latency_ms": 420,
    }
