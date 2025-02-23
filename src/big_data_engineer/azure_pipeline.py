from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List


@dataclass
class AzurePipelineResult:
    raw_rows: int
    clean_rows: int
    gold_rows: int
    total_revenue: float
    regions: List[str] = field(default_factory=list)
    bronze_path: str = "abfss://raw@contosodata.dfs.core.windows.net/bronze/"
    silver_path: str = "abfss://curated@contosodata.dfs.core.windows.net/silver/"
    gold_path: str = "abfss://curated@contosodata.dfs.core.windows.net/gold/"

    def as_dict(self) -> Dict[str, Any]:
        return {
            "raw_rows": self.raw_rows,
            "clean_rows": self.clean_rows,
            "gold_rows": self.gold_rows,
            "total_revenue": self.total_revenue,
            "regions": self.regions,
            "bronze_path": self.bronze_path,
            "silver_path": self.silver_path,
            "gold_path": self.gold_path,
        }


def _normalize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(row)
    normalized["amount"] = float(normalized.get("amount", 0) or 0)
    normalized["region"] = str(normalized.get("region", "Unknown")).strip() or "Unknown"
    normalized["event_id"] = str(normalized.get("event_id", "unknown-event")).strip()
    normalized["customer_id"] = str(normalized.get("customer_id", "unknown-customer")).strip()
    normalized["order_id"] = str(normalized.get("order_id", "unknown-order")).strip()
    return normalized


def build_end_to_end_pipeline_summary(rows: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    """Model a bronze -> silver -> gold pipeline summary for Azure analytics workloads."""

    raw_rows = list(rows)
    clean_rows: List[Dict[str, Any]] = []

    for raw_row in raw_rows:
        if raw_row is None:
            continue
        candidate = _normalize_row(raw_row)
        if candidate["amount"] <= 0:
            continue
        clean_rows.append(candidate)

    gold_rows = clean_rows
    total_revenue = round(sum(float(row.get("amount", 0) or 0) for row in gold_rows), 2)
    regions = sorted({str(row.get("region")) for row in gold_rows if row.get("region") is not None})

    result = AzurePipelineResult(
        raw_rows=len(raw_rows),
        clean_rows=len(clean_rows),
        gold_rows=len(gold_rows),
        total_revenue=total_revenue,
        regions=regions,
    )
    return result.as_dict()


def write_end_to_end_pipeline_summary(rows: Iterable[Dict[str, Any]]) -> AzurePipelineResult:
    summary = build_end_to_end_pipeline_summary(rows)
    return AzurePipelineResult(
        raw_rows=summary["raw_rows"],
        clean_rows=summary["clean_rows"],
        gold_rows=summary["gold_rows"],
        total_revenue=summary["total_revenue"],
        regions=summary["regions"],
    )
