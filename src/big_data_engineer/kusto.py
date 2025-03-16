from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class KustoQuery:
    name: str
    query: str


def build_kusto_queries() -> List[KustoQuery]:
    return [
        KustoQuery(
            name="recent_errors",
            query=(
                "Telemetry | where Timestamp > ago(24h) | where Level == 'Error' "
                "| summarize failures=count() by bin(Timestamp, 1h), MachineName | order by Timestamp desc"
            ),
        ),
        KustoQuery(
            name="top_failed_operations",
            query=(
                "Telemetry | where Timestamp > ago(7d) | where Success == false "
                "| summarize failed=count() by OperationName | top 10 by failed desc"
            ),
        ),
        KustoQuery(
            name="high_volume_queries",
            query=(
                "Telemetry | where Timestamp > ago(1d) | summarize requests=count() by QueryName "
                "| top 20 by requests desc"
            ),
        ),
    ]


def build_kusto_alert_rule() -> Dict[str, str]:
    return {
        "name": "spark_processing_anomaly",
        "query": "Telemetry | where Timestamp > ago(1h) | summarize rows=count() by bin(Timestamp, 5m) | where rows > 1000",
        "severity": "Sev2",
    }
