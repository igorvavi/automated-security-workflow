import argparse
from pathlib import Path
import json

from utils.logger import setup_logger
from scanners.nmap_scan import run_nmap
from scanners.dirbuster import run_dirbuster
from analysis.log_parser import parse_nmap_xml, parse_dirbuster_txt
from analysis.vuln_report_generator import synthesize_findings, write_json, write_markdown

def main():
    parser = argparse.ArgumentParser(description="Automated Security Workflow Pipeline")
    parser.add_argument("--target", "-t", default="127.0.0.1", help="Target host/IP")
    parser.add_argument("--out", "-o", default="out", help="Output directory")
    parser.add_argument("--nmap", action="store_true", help="Enable nmap TCP scan")
    parser.add_argument("--dirb", action="store_true", help="Enable simple dir brute")
    parser.add_argument("--wordlist", help="Wordlist path for dir brute")
    parser.add_argument("--use-samples-if-missing", action="store_true", help="Use sample results if tools not present")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    logger = setup_logger(str(out_dir / "log.txt"), verbose=args.verbose)

    logger.info("== Automated Security Workflow ==")
    logger.info(f"Target: {args.target}")
    logger.info(f"Output: {out_dir}")

    # Load config (optional)
    cfg_path = Path("config.json")
    config = {}
    if cfg_path.exists():
        config = json.loads(cfg_path.read_text())

    # Run scans
    nmap_xml = None
    dirb_txt = None
    if args.nmap:
        logger.info("[1/2] Running nmap scan...")
        nmap_xml = run_nmap(
            target=args.target,
            out_dir=str(out_dir),
            top_ports=int(config.get("nmap", {}).get("top_ports", 1000)),
            timing=str(config.get("nmap", {}).get("timing", "T3")),
            use_samples_if_missing=args.use_samples_if_missing
        )
        logger.info(f"nmap output: {nmap_xml}")

    if args.dirb:
        logger.info("[2/2] Running dir brute...")
        dirb_txt = run_dirbuster(
            base_url=f"http://{args.target}",
            out_dir=str(out_dir),
            wordlist=Path(args.wordlist) if args.wordlist else None,
            use_samples_if_missing=args.use_samples_if_missing
        )
        logger.info(f"dir brute output: {dirb_txt}")

    # Parse
    parsed_nmap = parse_nmap_xml(nmap_xml) if nmap_xml else {"host": None, "ports": []}
    parsed_paths = parse_dirbuster_txt(dirb_txt) if dirb_txt else []

    # Synthesize report
    report = synthesize_findings(parsed_nmap, parsed_paths)
    write_json(report, out_dir / "report.json")
    write_markdown(report, out_dir / "report.md")

    logger.info("Done. Reports written to report.json and report.md")

if __name__ == "__main__":
    main()
