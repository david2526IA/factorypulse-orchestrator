"""One-command orchestration with explicit artifacts and run manifest."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from factorypulse_ingestion.pipeline import emit_jsonl
from factorypulse_intelligence.pipeline import analyse_parquet
from factorypulse_lakehouse.pipeline import run_pipeline


def run(workspace: str | Path, count: int = 120, fault_after: int | None = 85) -> dict[str, object]:
    """Run the entire reference flow and prepare the API's read-only data mount."""
    if count < 8:
        raise ValueError("count must be at least 8 for the anomaly baseline")
    root = Path(workspace)
    root.mkdir(parents=True, exist_ok=True)
    telemetry = root / "telemetry.jsonl"
    warehouse = root / "warehouse"
    anomalies = root / "anomalies.jsonl"
    ingest = emit_jsonl(telemetry, count=count, fault_after=fault_after)
    lakehouse = run_pipeline(telemetry, warehouse)
    intelligence = analyse_parquet(warehouse / "silver_telemetry.parquet", anomalies)
    api_data = root / "api-data"
    api_data.mkdir(exist_ok=True)
    for source, destination in (
        (warehouse / "warehouse.duckdb", api_data / "warehouse.duckdb"),
        (warehouse / "data_quality_event.json", api_data / "data_quality_event.json"),
        (anomalies, api_data / "anomalies.jsonl"),
    ):
        shutil.copy2(source, destination)
    manifest = {
        "run_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "parameters": {"count": count, "fault_after": fault_after},
        "ingestion": ingest,
        "lakehouse": lakehouse,
        "intelligence": intelligence,
        "api_data_dir": str(api_data),
    }
    (root / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest
