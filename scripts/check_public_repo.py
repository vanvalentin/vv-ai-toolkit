#!/usr/bin/env python3
"""Fail on high-confidence secrets or private deployment identifiers.

This is intentionally dependency-free so it can run locally and in GitHub Actions.
It complements, rather than replaces, manual review and a maintained secret scanner.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_FILE_BYTES = 2_000_000

SKIP_SUFFIXES = {
    ".bmp", ".gif", ".ico", ".jpeg", ".jpg", ".pdf", ".png", ".webp",
    ".pyc", ".zip",
}

SENSITIVE_FILENAMES = {
    ".env", "auth.json", "credentials.json", "discord.token", "cookies.json",
}

# Optional client integrations belong inside their toolkit, not at repository root.
FORBIDDEN_ROOT_PATHS = (".agents", ".claude", ".codex", ".cursor", ".mcp.json")

RULES: list[tuple[str, re.Pattern[str]]] = [
    ("private key material", re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("GitHub token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b")),
    ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{20,}\b")),
    ("credential embedded in URL", re.compile(r"https?://[^\s/@:]+:[^\s/@]+@", re.I)),
    ("private IPv4 address", re.compile(
        r"\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})\b"
    )),
    ("non-placeholder Linux home path", re.compile(r"/home/(?!user(?:/|\b)|example(?:/|\b))[A-Za-z0-9._-]+/")),
    ("non-placeholder macOS home path", re.compile(r"/Users/(?!user(?:/|\b)|example(?:/|\b))[A-Za-z0-9._-]+/")),
]

EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b")
LONG_IDENTIFIER = re.compile(r"(?<!\d)\d{17,20}(?!\d)")
SAFE_EMAIL_DOMAINS = {"example.com", "example.org", "example.net", "users.noreply.github.com"}

SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(?:api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|password|passwd|secret)\b"
    r"\s*[=:]\s*[\"']([^\"']+)[\"']"
)
SAFE_VALUE_MARKERS = ("REPLACE", "EXAMPLE", "CHANGEME", "${", "<", "NONE")


def candidate_paths() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [ROOT / item.decode("utf-8") for item in result.stdout.split(b"\0") if item]


def scan(path: Path) -> list[str]:
    rel = path.relative_to(ROOT).as_posix()
    findings: list[str] = []

    if path.name.lower() in SENSITIVE_FILENAMES and not rel.endswith(".env.example"):
        findings.append("sensitive filename")

    if path.suffix.lower() in SKIP_SUFFIXES or not path.is_file():
        return findings
    if path.stat().st_size > MAX_FILE_BYTES:
        return findings

    raw = path.read_bytes()
    if b"\0" in raw:
        return findings
    text = raw.decode("utf-8", errors="replace")

    for label, pattern in RULES:
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            findings.append(f"line {line}: {label}")

    for match in EMAIL.finditer(text):
        if match.group(1).lower() not in SAFE_EMAIL_DOMAINS:
            line = text.count("\n", 0, match.start()) + 1
            findings.append(f"line {line}: non-placeholder email address")

    # Long numeric IDs commonly expose chat, account, or cloud-resource identifiers.
    # Dependency lock files can legitimately contain numeric hash fragments.
    if path.suffix.lower() != ".lock":
        for match in LONG_IDENTIFIER.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            findings.append(f"line {line}: long account or service identifier")

    for match in SECRET_ASSIGNMENT.finditer(text):
        value = match.group(1).strip()
        if len(value) >= 8 and not any(marker in value.upper() for marker in SAFE_VALUE_MARKERS):
            line = text.count("\n", 0, match.start()) + 1
            findings.append(f"line {line}: apparent literal secret assignment")

    return findings


def main() -> int:
    all_findings: list[tuple[str, str]] = []
    for rel in FORBIDDEN_ROOT_PATHS:
        if (ROOT / rel).exists():
            all_findings.append((rel, "optional client integration must be toolkit-local"))

    for path in candidate_paths():
        for finding in scan(path):
            all_findings.append((path.relative_to(ROOT).as_posix(), finding))

    if all_findings:
        print("Public-repository privacy check failed:", file=sys.stderr)
        for path, finding in all_findings:
            print(f"- {path}: {finding}", file=sys.stderr)
        return 1

    print("Public-repository privacy check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
