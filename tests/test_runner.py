import json

from factorypulse_api.repository import anomalies, quality
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
    api_settings = Settings.from_directory(root / "api-data")
    assert quality(api_settings)["accepted_rows"] == 20
    assert len(anomalies(api_settings)["events"]) == manifest["intelligence"]["anomalies"]
    assert json.loads((root / "run_manifest.json").read_text())["parameters"]["count"] == 20
