from pathlib import Path
import json
from typing import Dict, Any, List

def severity_for_port(port: int) -> str:
    if port in (22, 23):  # ssh/telnet
        return "medium" if port == 22 else "high"
    if port in (80, 443, 8080):
        return "medium"
    return "info"

def synthesize_findings(nmap: Dict[str, Any], paths: List[str]) -> Dict[str, Any]:
    findings = []
    for entry in nmap.get("ports", []):
        if entry.get("state") == "open":
            findings.append({
                "id": f"PORT-{entry['port']}",
                "title": f"Open port {entry['port']}/{entry['proto']}",
                "service": entry.get("service"),
                "severity": severity_for_port(entry["port"]),
                "recommendation": "Validate necessity, restrict access, and monitor with firewall rules.",
            })
    for p in paths:
        findings.append({
            "id": f"PATH-{p}",
            "title": f"Discovered path: {p}",
            "severity": "info",
            "recommendation": "Review exposure. If sensitive, enforce auth or remove.",
        })
    return {"summary": {"total": len(findings)}, "findings": findings}

def write_json(report: Dict[str, Any], out_json: Path):
    out_json.write_text(json.dumps(report, indent=2))

def write_markdown(report: Dict[str, Any], out_md: Path):
    lines = ["# Security Scan Report", ""]
    lines.append(f"Total findings: {report['summary']['total']}")
    lines.append("") 
    lines.append("| ID | Title | Severity | Recommendation |")
    lines.append("| --- | --- | --- | --- |")
    for f in report["findings"]:
        lines.append(f"| {f['id']} | {f['title']} | {f['severity']} | {f['recommendation']} |")
    out_md.write_text("\n".join(lines))
