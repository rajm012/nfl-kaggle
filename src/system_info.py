"""Print a compact remote resource inventory using the standard library only.

Run directly on the remote machine: python3 system_info.py
Does not inspect credentials, SSH configuration or environment variables.
"""
import json
import os
import platform
from pathlib import Path
import shutil
import subprocess


def main() -> None:
    cpu_available = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else os.cpu_count()
    info = {"os": platform.system(), "architecture": platform.machine(),
            "python": platform.python_version(), "logical_cpus_available": cpu_available,
            "free_disk_GiB_here": round(shutil.disk_usage(Path.cwd()).free / 2**30, 1)}
    meminfo = Path("/proc/meminfo")
    if meminfo.exists():
        fields = dict(line.split(":", 1) for line in meminfo.read_text().splitlines())
        for label, name in (("MemTotal", "system_RAM_GiB"), ("MemAvailable", "available_RAM_GiB")):
            info[name] = round(int(fields[label].split()[0]) * 1024 / 2**30, 1)
    if shutil.which("nvidia-smi"):
        try:
            result = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,driver_version",
                                     "--format=csv,noheader"], capture_output=True, text=True, timeout=10)
            info["gpu"] = result.stdout.strip() if result.returncode == 0 else "nvidia-smi query failed"
        except subprocess.TimeoutExpired:
            info["gpu"] = "nvidia-smi query timed out"
    else:
        info["gpu"] = "nvidia-smi unavailable"
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
