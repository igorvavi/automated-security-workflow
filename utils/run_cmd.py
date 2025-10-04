import subprocess
from typing import Tuple

def run(cmd: list, timeout: int = 60) -> Tuple[int, str, str]:
    """Run a command and return (returncode, stdout, stderr)."""
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        return 124, "", "Timeout expired"
    return proc.returncode, out, err
