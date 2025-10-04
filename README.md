# Automated Security Workflow

A minimal, educational automation pipeline that runs lightweight discovery, parses results, and generates a consolidated report.

> **Purpose:** Demonstrate backend scripting, automation, and Linux CLI orchestration using Python

## ✨ Features
- Pluggable **scanner modules** (start with `nmap` wrapper and a simple HTTP directory brute prototype).
- Central **pipeline orchestrator** (`pipeline.py`) with CLI flags.
- **Parsing & reporting** to JSON and Markdown.
- Structured **logging** and basic error handling.
- Works with real tools if present (e.g., `nmap`), but also supports **sample inputs** for offline demo.

## 📦 Project Structure
```
automated-security-workflow/
├─ scanners/
│  ├─ nmap_scan.py
│  ├─ dirbuster.py
├─ analysis/
│  ├─ log_parser.py
│  ├─ vuln_report_generator.py
├─ utils/
│  ├─ logger.py
│  ├─ run_cmd.py
├─ samples/
│  ├─ nmap_sample.xml
│  ├─ dirbuster_sample.txt
├─ tests/
│  ├─ test_pipeline.py
├─ pipeline.py
├─ config.json
├─ requirements.txt
└─ README.md
```

## 🚀 Quickstart
```bash
# (Optional) create venv
python -m venv .venv && source .venv/bin/activate

# install requirements (stdlib only by default)
pip install -r requirements.txt

# run pipeline with example target (uses live tools if available, else sample files)
python pipeline.py --target 127.0.0.1 --out out --use-samples-if-missing
```

Outputs:
- `out/report.json`
- `out/report.md`
- `out/log.txt`

## 🧰 CLI Options
```
python pipeline.py --help
```
- `--target / -t` : Target host/IP (default: 127.0.0.1)
- `--out / -o`    : Output folder (default: out)
- `--nmap`        : Enable nmap TCP scan
- `--dirb`        : Enable simple directory brute (wordlist-based)
- `--wordlist`    : Path to wordlist (for dir brute)
- `--use-samples-if-missing` : Use sample results when tools are absent
- `--verbose`     : Verbose logging

## 🧪 Samples
Real tools aren't always available on interview machines. The pipeline can parse **pre-recorded** outputs under `samples/`:
- `nmap_sample.xml` (host + 2 open ports)
- `dirbuster_sample.txt` (few discovered paths)

## 🧱 Design Notes
- Standard library only (no external deps): easier to review.
- The pipeline composes **independent steps** (scan → parse → report). Each module is testable in isolation.
- Logging via `utils/logger.py` writes both to console and file.

## 🧭 Roadmap
- [ ] Add UDP scan support
- [ ] Add HTTP title + status fetcher
- [ ] Export to HTML
- [ ] GitHub Actions CI (lint + unit tests)
- [ ] Containerize with Docker
- [ ] Optional: simple web UI for browsing reports

## 📜 License
MIT (for educational/demo purposes)
