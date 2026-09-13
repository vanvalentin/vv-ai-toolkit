"""Shared cross-platform paths for project scripts."""

import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = PROJECT_DIR.parent
VENV_DIR = WORKSPACE_DIR / ".venv"


def venv_executable(name: str, *, platform_name: str = os.name) -> Path:
    if platform_name == "nt":
        executable = f"{name}.exe" if name != "python" else "python.exe"
        return VENV_DIR / "Scripts" / executable
    return VENV_DIR / "bin" / name


VENV_PYTHON = venv_executable("python")
VENV_RUFF = venv_executable("ruff")
VENV_UVX = venv_executable("uvx")
