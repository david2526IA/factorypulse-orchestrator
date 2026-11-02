# FactoryPulse Orchestrator

> One-command, pinned-version end-to-end demonstration of the FactoryPulse platform.

[![End-to-end CI](https://github.com/david2526IA/factorypulse-orchestrator/actions/workflows/ci.yml/badge.svg)](https://github.com/david2526IA/factorypulse-orchestrator/actions/workflows/ci.yml)
[![FactoryPulse](https://img.shields.io/badge/platform-FactoryPulse-2563EB)](https://github.com/david2526IA/factorypulse-contracts)

This repository proves that FactoryPulse is more than a collection of isolated examples. It installs pinned versions of the upstream components and runs the complete path from simulated sensor telemetry to a read-only API-ready operational view.

## What one command does

```text
factorypulse-run run
        │
        ├── Ingestion: emits validated telemetry.v1 JSONL
        ├── Lakehouse: creates DuckDB/Parquet and data_quality.v1
        ├── Intelligence: publishes explainable anomaly.v1 JSONL
        └── API staging: prepares a read-only artifact directory
```

## Quick start

```bash
git clone https://github.com/david2526IA/factorypulse-orchestrator.git
cd factorypulse-orchestrator
python -m venv .venv
```

Activate the environment, then run:

```bash
pip install -e ".[dev]"
factorypulse-run run --workspace artifacts/demo --count 120 --fault-after 85
factorypulse-run serve --workspace artifacts/demo
pytest -q
```

Open `http://127.0.0.1:8000/docs` to inspect the API. The [FactoryPulse Dashboard](https://github.com/david2526IA/factorypulse-dashboard) can consume a compatible API URL through its `?api=` parameter.

## Run artifacts

```text
artifacts/demo/
├── telemetry.jsonl
├── anomalies.jsonl
├── warehouse/
│   ├── warehouse.duckdb
│   ├── silver_telemetry.parquet
│   └── gold_asset_health.parquet
├── api-data/
│   ├── warehouse.duckdb
│   ├── anomalies.jsonl
│   └── data_quality_event.json
└── run_manifest.json
```

The run manifest records parameters and outputs, making the demonstration reproducible and reviewable.

## Versioning decision

Each upstream dependency is pinned to a Git commit. This prevents an unrelated later change in a component from silently changing this end-to-end demo. Updating a component is therefore an explicit, reviewable decision.

## Safety boundary

FactoryPulse is a simulated, read-only reference platform. It has no actuator control capability and must not be connected to real operational equipment without a separate engineering, security and safety programme.

## License

MIT © 2026 David Falcon
