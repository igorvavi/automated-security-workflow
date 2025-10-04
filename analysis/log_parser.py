from pathlib import Path
from typing import Dict, Any, List
import xml.etree.ElementTree as ET

def parse_nmap_xml(xml_path: Path) -> Dict[str, Any]:
    data = {"host": None, "ports": []}
    tree = ET.parse(xml_path)
    root = tree.getroot()
    host = root.find("host")
    if host is None:
        return data
    addr = host.find("address")
    if addr is not None:
        data["host"] = addr.attrib.get("addr")
    ports = host.find("ports")
    if ports is None:
        return data
    for p in ports.findall("port"):
        portid = p.attrib.get("portid")
        proto = p.attrib.get("protocol")
        state = p.find("state").attrib.get("state") if p.find("state") is not None else "unknown"
        service = p.find("service").attrib.get("name") if p.find("service") is not None else None
        data["ports"].append({"port": int(portid), "proto": proto, "state": state, "service": service})
    return data

def parse_dirbuster_txt(txt_path: Path) -> List[str]:
    lines = Path(txt_path).read_text().splitlines()
    return [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")]
