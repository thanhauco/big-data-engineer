from big_data_engineer.azure_storage import AzureStorageConfig, build_adls_url, ensure_valid_container_name
from big_data_engineer.config import EnvironmentSettings, SparkJobConfig
from big_data_engineer.fabric import build_fabric_gold_table, build_fabric_dashboard_metrics
from big_data_engineer.kusto import build_kusto_queries
from big_data_engineer.spark_jobs import build_daily_revenue_summary


def test_storage_config_builds_adls_url():
    config = AzureStorageConfig("contoso", "raw-zone", "bronze/telemetry")
    assert config.adls_url.startswith("abfss://raw-zone@contoso.dfs.core.windows.net/")
    assert "bronze/telemetry" in config.adls_url


def test_container_validation_rejects_invalid_name():
    try:
        ensure_valid_container_name("Bad_Container")
        assert False, "Expected ValueError for invalid container name"
    except ValueError:
        pass


def test_build_adls_url_helper():
    path = build_adls_url("contoso", "curated", "gold")
    assert path == "abfss://curated@contoso.dfs.core.windows.net/gold"


def test_environment_settings_expose_azure_components():
    env = EnvironmentSettings()
    assert env.adls_root.startswith("abfss://raw@contosodata.dfs.core.windows.net/")
    assert env.synapse_database == "analyticsdb"


def test_spark_job_config_has_expected_fields():
    config = SparkJobConfig()
    assert config.partitions == 8
    assert "event_id" in config.required_columns()


def test_daily_revenue_summary():
    summary = build_daily_revenue_summary(
        [
            {"amount": 12.5, "region": "West", "event_id": "1"},
            {"amount": 18.0, "region": "East", "event_id": "2"},
        ],
        partition_col="date_partition",
    )
    assert summary["record_count"] == 2
    assert summary["total_revenue"] == 30.5
    assert "East" in summary["regions"]


def test_fabric_table_and_metrics():
    table = build_fabric_gold_table()
    assert "gold_orders" in table.as_sql()
    metrics = build_fabric_dashboard_metrics()
    assert metrics["orders_processed"] > 0


def test_kusto_queries_exist():
    queries = build_kusto_queries()
    assert len(queries) >= 3
    assert queries[0].name == "recent_errors"


def test_end_to_end_pipeline_summary():
    from big_data_engineer.azure_pipeline import build_end_to_end_pipeline_summary

    summary = build_end_to_end_pipeline_summary(
        [
            {"event_id": "evt-1", "customer_id": "cust-1", "order_id": "ord-1", "amount": 100.0, "region": "West"},
            {"event_id": "evt-2", "customer_id": "cust-2", "order_id": "ord-2", "amount": 60.0, "region": "East"},
            {"event_id": "evt-3", "customer_id": "cust-1", "order_id": "ord-3", "amount": 0.0, "region": "West"},
        ]
    )

    assert summary["raw_rows"] == 3
    assert summary["clean_rows"] == 2
    assert summary["gold_rows"] == 2
    assert summary["total_revenue"] == 160.0


def test_delta_lake_and_fabric_workflow_plan():
    from big_data_engineer.delta_pipeline import build_delta_write_plan

    plan = build_delta_write_plan(
        table_name="gold_sales",
        output_path="abfss://curated@contosodata.dfs.core.windows.net/gold/sales",
        partition_col="date_partition",
        mode="overwrite",
    )

    assert plan["table_name"] == "gold_sales"
    assert plan["format"] == "delta"
    assert plan["partition_col"] == "date_partition"
    assert "overwrite" in plan["write_mode"]
    assert "sales" in plan["output_path"]
