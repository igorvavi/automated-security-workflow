# Minimal smoke test (can expand later)
import subprocess, sys, os, json, pathlib

def test_pipeline_samples(tmp_path):
    out = tmp_path / "out"
    cmd = [sys.executable, "pipeline.py", "--nmap", "--dirb", "--use-samples-if-missing", "--out", str(out)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    assert proc.returncode == 0
    assert (out / "report.json").exists()
    data = json.loads((out / "report.json").read_text())
    assert "findings" in data and len(data["findings"]) >= 1
