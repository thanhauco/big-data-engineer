from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class CosmosContainerConfig:
    account_name: str
    database_name: str
    container_name: str
    partition_key: str = "/customerId"
    throughput: int = 400

    @property
    def endpoint(self) -> str:
        return f"https://{self.account_name}.documents.azure.com:443/"

    def item_document(self, item_id: str, **fields: Any) -> Dict[str, Any]:
        payload = {"id": item_id, "customerId": fields.get("customerId", "anonymous")}
        payload.update(fields)
        return payload


def build_cosmos_query(customer_id: str, status: str = "processed") -> str:
    return (
        f"SELECT * FROM c WHERE c.customerId = '{customer_id}' AND c.status = '{status}' "
        "ORDER BY c._ts DESC"
    )


def get_cosmos_container_names() -> List[str]:
    return ["orders", "customers", "shipments", "invoices"]
