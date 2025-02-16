from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AzureStorageConfig:
    """Common ADLS / Cosmos connectivity metadata for Azure analytics workloads."""

    account_name: str
    container_name: str
    directory: str = "raw"
    public_endpoint: str = "core.windows.net"

    def __post_init__(self) -> None:
        self.container_name = ensure_valid_container_name(self.container_name)

    @property
    def adls_url(self) -> str:
        return (
            f"abfss://{self.container_name}@{self.account_name}.dfs.{self.public_endpoint}/"
            f"{self.directory}"
        )

    @property
    def blob_url(self) -> str:
        return (
            f"https://{self.account_name}.blob.{self.public_endpoint}/"
            f"{self.container_name}/{self.directory}"
        )

    def build_paths(self, file_name: str) -> Dict[str, str]:
        return {
            "adls": f"{self.adls_url}/{file_name}",
            "blob": f"{self.blob_url}/{file_name}",
        }


def ensure_valid_container_name(name: str) -> str:
    normalized = name.strip().lower()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,61}[a-z0-9]", normalized):
        raise ValueError(f"Invalid Azure container name: {name}")
    return normalized


def build_adls_url(account_name: str, container_name: str, directory: str = "raw") -> str:
    config = AzureStorageConfig(account_name=account_name, container_name=container_name, directory=directory)
    return config.adls_url


def list_storage_tiers() -> List[str]:
    return ["bronze", "silver", "gold", "curated"]
