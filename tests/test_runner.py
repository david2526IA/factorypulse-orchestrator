import json

from fastapi.testclient import TestClient

from factorypulse_api.app import create_app
from factorypulse_api.settings import Settings
from factorypulse_orchestrator.runner import run


def test_runner_produces_complete_api_ready_artifact_set(tmp_path) -> None:
    manifest = run(tmp_path / "run", count=20, fault_after=14)
    root = tmp_path / "run"
    assert manifest["ingestion"]["events"] == 20
    assert manifest["lakehouse"]["accepted_rows"] == 20
    assert manifest["intelligence"]["anomalies"] > 0
    assert (root / "run_manifest.json").exists()
    assert (root / "api-data" / "warehouse.duckdb").exists()
    client = TestClient(create_app(Settings.from_directory(root / "api-data")))
    assert client.get("/health").json()["status"] == "ok"
    assert client.get("/v1/summary").json()["anomaly_count"] == manifest["intelligence"]["anomalies"]
    assert json.loads((root / "run_manifest.json").read_text())["parameters"]["count"] == 20
