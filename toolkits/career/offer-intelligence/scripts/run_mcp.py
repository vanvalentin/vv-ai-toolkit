"""Launch the MCP server with the project virtual environment."""

from __future__ import annotations

import os

from _paths import VENV_PYTHON


def main() -> None:
    if not VENV_PYTHON.is_file():
        raise SystemExit(
            "Missing .venv. Run: python offer-intelligence/scripts/setup.py"
        )
    os.execv(str(VENV_PYTHON), [str(VENV_PYTHON), "-m", "offer_intel"])


if __name__ == "__main__":
    main()
