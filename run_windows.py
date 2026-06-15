from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path


SUPPORTED_PYTHONS = {"3.12", "3.11"}


def find_project_root() -> Path:
    start = Path(__file__).resolve().parent
    for base in (start, *start.parents):
        if (base / "V-0.1" / "MediaPipeFolder" / "main.py").is_file():
            return base / "V-0.1"
        if (base / "MediaPipeFolder" / "main.py").is_file():
            return base
        if (base / "MediaPipe" / "main.py").is_file():
            return base
    return start


def find_entry_file(project_root: Path) -> Path:
    candidates = (
        project_root / "MediaPipeFolder" / "main.py",
        project_root / "MediaPipe" / "main.py",
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("Could not locate a main.py entry point.")


def venv_python(project_root: Path) -> Path:
    return project_root / ".venv" / "Scripts" / "python.exe"


def _python_version(command: list[str]) -> str | None:
    probe = subprocess.run(
        command + ["-c", "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')"],
        capture_output=True,
        text=True,
    )
    if probe.returncode != 0:
        return None
    return probe.stdout.strip()


def select_bootstrap_python() -> list[str]:
    current_version = f"{sys.version_info[0]}.{sys.version_info[1]}"
    if current_version in SUPPORTED_PYTHONS:
        return [sys.executable]

    py_launcher = shutil.which("py")
    if py_launcher:
        for version in ("3.12", "3.11"):
            probe = subprocess.run(
                [py_launcher, f"-{version}", "-c", "import sys; print(sys.version_info[:2])"],
                capture_output=True,
                text=True,
            )
            if probe.returncode == 0:
                return [py_launcher, f"-{version}"]

    for candidate in ("python3.12", "python3.11"):
        path = shutil.which(candidate)
        if path and _python_version([path]) in SUPPORTED_PYTHONS:
            return [path]

    raise RuntimeError(
        "No supported Python 3.11/3.12 interpreter was found. "
        "Install Python 3.11 or 3.12, then rerun the launcher."
    )


def ensure_venv(project_root: Path) -> Path:
    python_bin = venv_python(project_root)
    if python_bin.is_file():
        return python_bin

    print("Creating local virtual environment...")
    bootstrap_python = select_bootstrap_python()
    subprocess.run(bootstrap_python + ["-m", "venv", str(project_root / ".venv")], check=True)
    return python_bin


def install_requirements(project_root: Path, python_bin: Path) -> None:
    requirements = project_root.parent / "requirements.txt"
    if not requirements.is_file():
        requirements = project_root / "requirements.txt"

    if not requirements.is_file():
        raise FileNotFoundError("requirements.txt was not found.")

    stamp_file = project_root / ".venv" / ".requirements.sha256"
    requirements_hash = hashlib.sha256(requirements.read_bytes()).hexdigest()
    if stamp_file.is_file() and stamp_file.read_text(encoding="utf-8").strip() == requirements_hash:
        return

    print("Installing requirements...")
    subprocess.run([str(python_bin), "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([str(python_bin), "-m", "pip", "install", "-r", str(requirements)], check=True)
    stamp_file.write_text(requirements_hash, encoding="utf-8")


def main() -> None:
    print("Starting project on Windows...")

    project_root = find_project_root()
    entry_file = find_entry_file(project_root)
    entry_dir = entry_file.parent

    print(f"Project root: {project_root}")
    print(f"Entry point: {entry_file}")

    python_bin = ensure_venv(project_root)
    install_requirements(project_root, python_bin)

    os.chdir(entry_dir)
    if str(entry_dir) not in sys.path:
        sys.path.insert(0, str(entry_dir))
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    os.execv(str(python_bin), [str(python_bin), str(entry_file)])


if __name__ == "__main__":
    main()
