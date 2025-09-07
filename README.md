# Big Data Engineer Portfolio Repository

This repository is a hands-on, cloud-native data engineering project built around the Microsoft Azure analytics stack. It demonstrates end-to-end patterns for ingesting, transforming, validating, and monitoring large-scale data using Synapse, Spark, ADLS, Cosmos, Kusto, and Fabric.

## Role Alignment

This project directly addresses the target skill set for a Big Data Engineer role in Redmond, WA:

- Synapse Analytics
- Scala
- Spark / PySpark
- SQL / Scope
- Cosmos DB / ADLS
- Kusto / Azure Data Explorer
- Microsoft Fabric / OneLake

## Business Problem

The repository models a retail and telemetry analytics platform where raw event data is ingested from multiple sources, processed into curated layers, and exposed to business reporting and operational monitoring workflows.

## Architecture Overview

```text
ADLS / Cosmos ingestion
        |
        v
Spark ETL (PySpark + Scala)
        |
        +--> Synapse SQL / Fabric Lakehouse
        |
        +--> Kusto metrics and alerts
        |
        +--> Curated gold datasets for reporting
```

## Repository Structure

- `src/big_data_engineer/` — Python reference package for Azure configs, Spark jobs, Cosmos patterns, Kusto, and Fabric
- `examples/` — runnable sample pipeline entry points
- `data/` — sample data files
- `scala/` — Scala/Spark example implementation
- `sql/` — Synapse and Fabric SQL examples
- `kql/` — Kusto queries and alerting logic
- `tests/` — Build validation and regression checks
- `architecture.md` — architecture diagrams, analysis, and role-aligned system storytelling
- `fabric_workflow.md` — Microsoft Fabric / OneLake workflow notes and notebook-style pattern
- `PROJECT_SUMMARY.md` — interview-ready role summary
- `GITHUB_PROJECT_SUMMARY.md` — concise GitHub/portfolio summary for hiring visibility

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src pytest -q
python3 examples/delta_pipeline.py
```

## Example Use Cases

- ADLS landing zone and storage pattern validation
- Daily sales aggregation in PySpark
- Partition-aware bronze-to-gold processing
- Synapse/Fabric SQL transformations and curated views
- Cosmos query design for transactional and document workloads
- Kusto monitoring for operational insights

## Project Highlights

### 1. Azure Data Platform Patterns
The modules under `src/big_data_engineer/` provide realistic Azure configuration and validation patterns for ADLS, Synapse, Cosmos, and Fabric.

### 2. Spark ETL Modeling
The Spark logic models typical revenue, telemetry, and order-processing workloads using partitioning and curated outputs.

### 3. Delta and Fabric Workflow Design
The Delta pipeline examples show how gold-layer datasets can be written in Delta format and then surfaced through Microsoft Fabric OneLake workflows.

### 4. Data Warehouse and OneLake SQL
The SQL examples show warehouse-friendly patterns for incremental load, aggregated views, and lakehouse-friendly design.

### 5. Operational Analytics with Kusto
The KQL files provide examples for recent errors, failed operations, volume spikes, and threshold-based detection.

## Verification

The repository is currently validated with automated tests and CI automation:

```bash
PYTHONPATH=src python3 -m pytest -q
python3 examples/delta_pipeline.py
```

Current result: 10 tests passed.

A GitHub Actions workflow also runs the same verification automatically on push and pull request.

## Notes

This repository is structured as a portfolio-ready starter project for cloud data engineering interviews, architecture discussions, and role-specific practice.
