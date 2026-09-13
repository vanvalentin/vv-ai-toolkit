"""Run all project checks on Windows or macOS."""

from __future__ import annotations

import subprocess

from _paths import PROJECT_DIR, VENV_PYTHON, VENV_RUFF, WORKSPACE_DIR


def run(*args: str) -> None:
    subprocess.run(args, cwd=WORKSPACE_DIR, check=True)


def main() -> None:
    if not VENV_PYTHON.is_file():
        raise SystemExit(
            "Missing .venv. Run: python offer-intelligence/scripts/setup.py"
        )
    run(str(VENV_PYTHON), "-m", "pytest", str(PROJECT_DIR / "tests"))
    run(
        str(VENV_RUFF),
        "check",
        str(PROJECT_DIR / "src"),
        str(PROJECT_DIR / "tests"),
        str(PROJECT_DIR / "evals" / "run_eval.py"),
        str(PROJECT_DIR / "scripts"),
    )
    run(str(VENV_PYTHON), str(PROJECT_DIR / "evals" / "run_eval.py"))
    run(str(VENV_PYTHON), "-m", "pip", "check")


if __name__ == "__main__":
    main()
