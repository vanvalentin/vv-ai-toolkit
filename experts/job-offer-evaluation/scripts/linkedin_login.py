"""Launch the upstream LinkedIn manual login on Windows or macOS."""

from __future__ import annotations

import subprocess

from _paths import REPO_ROOT, VENV_UVX


def main() -> None:
    if not VENV_UVX.is_file():
        raise SystemExit(
            "Missing uvx. Run: python experts/job-offer-evaluation/scripts/setup.py"
        )
    result = subprocess.run(
        [str(VENV_UVX), "mcp-server-linkedin@latest", "--login"],
        cwd=REPO_ROOT,
        check=False,
    )
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
