from pathlib import Path
from typing import Optional
from utils.run_cmd import run

def which(program: str) -> Optional[str]:
    import shutil
    return shutil.which(program)

def run_nmap(target: str, out_dir: str, top_ports: int = 1000, timing: str = "T3", use_samples_if_missing: bool = False) -> Path:
    out_xml = Path(out_dir) / "nmap.xml"
    nmap_path = which("nmap")
    if nmap_path is None:
        if use_samples_if_missing:
            # copy sample file to out
            sample = Path(__file__).resolve().parents[1] / "samples" / "nmap_sample.xml"
            out_xml.write_text(sample.read_text())
            return out_xml
        raise RuntimeError("nmap not found and samples disabled")
    # -Pn: skip host discovery to avoid needing root, -oX: XML output
    code, out, err = run([nmap_path, "-Pn", f"--top-ports={top_ports}", f"-{timing}", "-oX", str(out_xml), target], timeout=300)
    if code != 0:
        raise RuntimeError(f"nmap failed: {err.strip()}")
    return out_xml
