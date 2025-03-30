from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


@dataclass
class DeltaWritePlan:
    table_name: str
    output_path: str
    partition_col: str
    mode: str = "overwrite"
    format: str = "delta"

    def as_dict(self) -> Dict[str, Any]:
        return {
            "table_name": self.table_name,
            "output_path": self.output_path,
            "partition_col": self.partition_col,
            "write_mode": self.mode,
            "format": self.format,
        }


def build_delta_write_plan(
    table_name: str,
    output_path: str,
    partition_col: str = "date_partition",
    mode: str = "overwrite",
) -> Dict[str, Any]:
    plan = DeltaWritePlan(
        table_name=table_name,
        output_path=output_path,
        partition_col=partition_col,
        mode=mode,
        format="delta",
    )
    return plan.as_dict()


def write_delta_gold_table(
    records: Iterable[Dict[str, Any]],
    output_path: str,
    table_name: str = "gold_sales",
    partition_col: str = "date_partition",
    mode: str = "overwrite",
) -> Dict[str, Any]:
    """Create a Spark DataFrame, write it to a Delta table path, and return metadata."""

    rows: List[Dict[str, Any]] = list(records)
    spark = (
        SparkSession.builder.appName("DeltaGoldWrite")
        .master("local[*]")
        .config("spark.jars.packages", "io.delta:delta-spark_2.13:4.0.0")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .getOrCreate()
    )

    try:
        df = spark.createDataFrame(rows)
        if partition_col not in df.columns:
            df = df.withColumn(partition_col, df["event_ts"]) if "event_ts" in df.columns else df.withColumn(partition_col, F.lit("2026-09-14"))

        df.write.mode(mode).format("delta").partitionBy(partition_col).save(output_path)
        row_count = df.count()
    finally:
        spark.stop()

    plan = build_delta_write_plan(
        table_name=table_name,
        output_path=output_path,
        partition_col=partition_col,
        mode=mode,
    )
    plan["rows_written"] = row_count
    plan["status"] = "success"
    return plan


def build_fabric_workflow_steps() -> Dict[str, Any]:
    return {
        "step_1": "Read curated Gold table from ADLS Delta location",
        "step_2": "Create or replace lakehouse table in Microsoft Fabric OneLake",
        "step_3": "Publish semantic model and business metrics for dashboard consumption",
        "step_4": "Schedule refresh and monitor quality checks in Kusto",
    }
