"""Run deterministic factuality checks against anonymized golden cases."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from offer_intel.models import EvidencePack, ReportDraft
from offer_intel.validation import validate_report


def evaluate_fixture(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    pack = EvidencePack(
        case=payload["case"],
        sources=payload["sources"],
        evidence=payload["evidence"],
    )
    good = validate_report(ReportDraft.model_validate(payload["good_report"]), pack)
    bad = validate_report(ReportDraft.model_validate(payload["bad_report"]), pack)
    passed = good.valid and not bad.valid and good.citation_coverage == 100
    return {
        "fixture": path.name,
        "passed": passed,
        "good_report_valid": good.valid,
        "bad_report_rejected": not bad.valid,
        "citation_coverage": good.citation_coverage,
        "bad_report_issue_codes": sorted({issue.code for issue in bad.issues}),
    }


def main() -> None:
    fixtures = sorted(Path(__file__).parent.glob("*.json"))
    results = [evaluate_fixture(path) for path in fixtures]
    print(json.dumps({"passed": all(item["passed"] for item in results), "results": results}))
    if not all(item["passed"] for item in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
