from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List


@dataclass
class SparkTransformationResult:
    source_path: str
    target_path: str
    rows_read: int
    rows_written: int
    metrics: Dict[str, int] = field(default_factory=dict)


@dataclass
class SparkETLJob:
    """Representative Spark ETL job modeling a curated lakehouse pipeline."""

    source_path: str
    output_path: str
    partition_cols: List[str] = field(default_factory=lambda: ["date_partition", "region"])
    watermark_days: int = 30

    def ingest(self, records: Iterable[Dict[str, object]]) -> SparkTransformationResult:
        items = list(records)
        rows_read = len(items)
        rows_written = rows_read
        metrics = {
            "filtered_rows": max(rows_read - 1, 0),
            "distinct_customers": len({str(item.get("customer_id")) for item in items if item.get("customer_id") is not None}),
            "aggregated_regions": len({str(item.get("region")) for item in items if item.get("region") is not None}),
        }
        return SparkTransformationResult(
            source_path=self.source_path,
            target_path=self.output_path,
            rows_read=rows_read,
            rows_written=rows_written,
            metrics=metrics,
        )

    def build_daily_revenue_summary(self, data: Iterable[Dict[str, object]]) -> Dict[str, object]:
        rows = list(data)
        total_revenue = sum(float(row.get("amount", 0) or 0) for row in rows)
        return {
            "record_count": len(rows),
            "total_revenue": round(total_revenue, 2),
            "regions": sorted({str(row.get("region")) for row in rows if row.get("region") is not None}),
            "daily_partition": self.partition_cols[0] if self.partition_cols else "date_partition",
        }


def build_daily_revenue_summary(data: Iterable[Dict[str, object]], partition_col: str = "date_partition") -> Dict[str, object]:
    rows = list(data)
    total = sum(float(row.get("amount", 0) or 0) for row in rows)
    return {
        "record_count": len(rows),
        "total_revenue": round(total, 2),
        "regions": sorted({str(row.get("region")) for row in rows if row.get("region") is not None}),
        "partition_col": partition_col,
    }
