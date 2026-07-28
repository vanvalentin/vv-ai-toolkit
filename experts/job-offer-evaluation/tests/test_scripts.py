import py_compile
import runpy
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
SCRIPTS = PROJECT_DIR / "scripts"


def test_scripts_compile_on_all_supported_python_versions() -> None:
    for script in SCRIPTS.glob("*.py"):
        py_compile.compile(str(script), doraise=True)


def test_virtual_environment_paths_cover_windows_and_macos() -> None:
    namespace = runpy.run_path(str(SCRIPTS / "_paths.py"))
    venv_executable = namespace["venv_executable"]

    assert venv_executable("python", platform_name="nt").as_posix().endswith(
        ".venv/Scripts/python.exe"
    )
    assert venv_executable("ruff", platform_name="nt").as_posix().endswith(
        ".venv/Scripts/ruff.exe"
    )
    assert venv_executable("python", platform_name="posix").as_posix().endswith(
        ".venv/bin/python"
    )
    assert venv_executable("ruff", platform_name="posix").as_posix().endswith(
        ".venv/bin/ruff"
    )
