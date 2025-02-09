from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class EnvironmentSettings:
    """Configuration model for Azure analytics platform components."""

    adls_account: str = "contosodata"
    adls_container: str = "raw"
    adls_path: str = "bronze/telemetry/"
    synapse_server: str = "contoso-synapse.sql.azuresynapse.net"
    synapse_database: str = "analyticsdb"
    cosmos_account: str = "contosocosmos"
    cosmos_database: str = "customer-events"
    cosmos_container: str = "orders"
    kusto_cluster: str = "https://contoso.kusto.windows.net"
    kusto_database: str = "telemetry"
    fabric_workspace: str = "SalesAnalytics"
    fabric_lakehouse: str = "OneLakeSales"

    def as_dict(self) -> Dict[str, str]:
        return {
            key: value for key, value in self.__dict__.items() if isinstance(value, str)
        }

    @property
    def adls_root(self) -> str:
        return f"abfss://{self.adls_container}@{self.adls_account}.dfs.core.windows.net/{self.adls_path}"


@dataclass
class SparkJobConfig:
    """Configuration used by Spark and ETL jobs."""

    app_name: str = "BigDataEngineerETL"
    source_path: str = "abfss://raw@contosodata.dfs.core.windows.net/bronze/telemetry/"
    output_path: str = "abfss://curated@contosodata.dfs.core.windows.net/gold/"
    partitions: int = 8
    watermark_days: int = 30
    business_date: str = "2026-09-14"
    extra_options: Dict[str, str] = field(default_factory=lambda: {"header": "true", "inferSchema": "true"})

    @property
    def partition_by(self) -> str:
        return f"date_partition={self.business_date}"

    def required_columns(self) -> List[str]:
        return ["event_id", "customer_id", "order_id", "event_ts", "amount", "region"]
