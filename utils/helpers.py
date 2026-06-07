import os
import sys
import hashlib
import subprocess
from core.ui import C

def get_system_info():
    import platform
    info = {
        "os": platform.platform(),
        "hostname": platform.node(),
        "arch": platform.machine(),
        "python": platform.python_version(),
        "kernel": platform.release(),
    }
    return info

def check_dependencies():
    deps = {
        "python3": "python --version",
        "nmap": "nmap --version",
        "whois": "whois --version",
        "curl": "curl --version",
        "git": "git --version",
    }
    available = []
    missing = []
    for name, cmd in deps.items():
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            if result.returncode == 0:
                available.append(name)
            else:
                missing.append(name)
        except:
            missing.append(name)
    return available, missing

def calculate_file_hash(filepath, algorithm="sha256"):
    h = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"

def validate_ip(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        try:
            num = int(part)
            if num < 0 or num > 255:
                return False
        except:
            return False
    return True

def validate_domain(domain):
    import re
    pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.match(pattern, domain))

def sanitize_input(text):
    dangerous_chars = [";", "&", "|", "$", "`", "(", ")", "{", "}", "<", ">"]
    for char in dangerous_chars:
        text = text.replace(char, "")
    return text

def colorize_severity(severity):
    colors = {
        "CRITICO": C.RED,
        "ALTO": C.ORANGE,
        "MEDIO": C.YELLOW,
        "BAJO": C.GREEN,
        "INFO": C.CYAN,
    }
    return colors.get(severity, C.WHITE)

def print_banner_small():
    print(f"""
{C.CYAN}{C.BOLD}  ████████╗███████╗██████╗ ██████╗  █████╗
  ╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔══██╗
     ██║   █████╗  ██████╔╝██████╔╝███████║
     ██║   ██╔══╝  ██╔══██╗██╔══██╗██╔══██║
     ██║   ███████╗██║  ██║██║  ██║██║  ██║
     ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝{C.RESET}
{C.DIM}  {C.SILVER}v2.0 Terminal Enhanced Cyber Command Hub{C.RESET}
""")
