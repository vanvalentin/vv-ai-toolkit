"""Process-local case registry; sensitive input is not persisted by default."""

from __future__ import annotations

from datetime import date, datetime
from threading import RLock
from typing import Any
from uuid import uuid4

from .models import (
    CaseInput,
    ClaimType,
    Confidence,
    Conflict,
    ConflictInput,
    EvidenceItem,
    EvidencePack,
    SourceKind,
    SourceRef,
)


class UnknownCaseError(KeyError):
    pass


class CaseRegistry:
    def __init__(self) -> None:
        self._cases: dict[str, EvidencePack] = {}
        self._lock = RLock()

    def create(self, case: CaseInput) -> tuple[str, EvidencePack]:
        case_id = f"CASE-{uuid4().hex[:12]}"
        pack = EvidencePack(case=case)
        with self._lock:
            self._cases[case_id] = pack
        return case_id, pack.model_copy(deep=True)

    def get(self, case_id: str) -> EvidencePack:
        with self._lock:
            try:
                return self._cases[case_id].model_copy(deep=True)
            except KeyError as exc:
                raise UnknownCaseError(case_id) from exc

    def add_evidence(
        self,
        case_id: str,
        *,
        source_title: str,
        source_kind: SourceKind,
        claim: str,
        excerpt: str,
        topic: str,
        url: str | None = None,
        publisher: str | None = None,
        published_at: datetime | date | None = None,
        observed_at: datetime | date | None = None,
        claim_type: ClaimType = ClaimType.FACT,
        confidence: Confidence = Confidence.MEDIUM,
        metadata: dict[str, Any] | None = None,
        upstream_version: str | None = None,
    ) -> EvidenceItem:
        with self._lock:
            try:
                pack = self._cases[case_id]
            except KeyError as exc:
                raise UnknownCaseError(case_id) from exc
            source = SourceRef(
                id=f"SRC-{uuid4().hex[:12]}",
                title=source_title,
                url=url,
                kind=source_kind,
                publisher=publisher,
                published_at=published_at,
                upstream_version=upstream_version,
            )
            item = EvidenceItem(
                id=f"EV-{uuid4().hex[:12]}",
                claim=claim,
                excerpt=excerpt,
                source_id=source.id,
                topic=topic,
                claim_type=claim_type,
                confidence=confidence,
                observed_at=observed_at,
                metadata=metadata or {},
            )
            pack.sources.append(source)
            pack.evidence.append(item)
            # Revalidate cross-references after mutation.
            self._cases[case_id] = EvidencePack.model_validate(pack.model_dump())
            return item.model_copy(deep=True)

    def add_blind_spot(self, case_id: str, message: str) -> EvidencePack:
        with self._lock:
            try:
                pack = self._cases[case_id]
            except KeyError as exc:
                raise UnknownCaseError(case_id) from exc
            if message not in pack.blind_spots:
                pack.blind_spots.append(message)
            return pack.model_copy(deep=True)

    def add_conflict(self, case_id: str, conflict: ConflictInput) -> Conflict:
        with self._lock:
            try:
                pack = self._cases[case_id]
            except KeyError as exc:
                raise UnknownCaseError(case_id) from exc
            known = {item.id for item in pack.evidence}
            unknown = sorted(set(conflict.evidence_ids) - known)
            if unknown:
                raise ValueError(f"Conflict cites unknown evidence IDs: {unknown}")
            stored = Conflict.model_validate(conflict.model_dump())
            pack.conflicts.append(stored)
            return stored.model_copy(deep=True)
