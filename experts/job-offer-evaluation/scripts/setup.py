"""Create and provision the project virtual environment."""

from __future__ import annotations

import subprocess
import sys

from _paths import PROJECT_DIR, REPO_ROOT, VENV_PYTHON


def run(*args: str) -> None:
    subprocess.run(args, cwd=REPO_ROOT, check=True)


def main() -> None:
    if VENV_PYTHON.is_file():
        print(f"Using existing virtual environment at {REPO_ROOT / '.venv'}", flush=True)
    else:
        run(sys.executable, "-m", "venv", str(REPO_ROOT / ".venv"))
    run(str(VENV_PYTHON), "-m", "pip", "install", "--upgrade", "pip")
    run(str(VENV_PYTHON), "-m", "pip", "install", "-e", str(PROJECT_DIR))
    run(str(VENV_PYTHON), "-m", "pip", "install", "pytest", "pytest-asyncio", "ruff")
    run(str(VENV_PYTHON), "-m", "patchright", "install", "chromium")
    print(f"Offer Intelligence is installed in {REPO_ROOT / '.venv'}")


if __name__ == "__main__":
    main()
