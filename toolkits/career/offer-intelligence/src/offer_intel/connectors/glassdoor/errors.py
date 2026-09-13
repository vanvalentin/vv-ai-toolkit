"""Structured connector exceptions safe to expose through an MCP tool."""

from __future__ import annotations

from typing import Any

from .models import ConnectorErrorInfo, ConnectorState, ErrorCode


class GlassdoorConnectorError(RuntimeError):
    def __init__(
        self,
        code: ErrorCode,
        message: str,
        *,
        state: ConnectorState = ConnectorState.UNAVAILABLE,
        retryable: bool = False,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.info = ConnectorErrorInfo(
            code=code,
            message=message,
            state=state,
            retryable=retryable,
            details=details or {},
        )

    def as_dict(self) -> dict[str, Any]:
        return self.info.model_dump(mode="json")


class AuthenticationRequired(GlassdoorConnectorError):
    def __init__(self, message: str = "A manual Glassdoor login is required.") -> None:
        super().__init__(
            ErrorCode.AUTH_REQUIRED,
            message,
            state=ConnectorState.UNAUTHENTICATED,
        )


class ChallengeDetected(GlassdoorConnectorError):
    def __init__(self, message: str = "Glassdoor presented a verification challenge.") -> None:
        super().__init__(
            ErrorCode.CHALLENGE_DETECTED,
            message,
            state=ConnectorState.CHALLENGE,
            details={"action": "Complete the challenge manually; it will not be bypassed."},
        )


class UnsupportedPage(GlassdoorConnectorError):
    def __init__(self, url: str) -> None:
        super().__init__(
            ErrorCode.UNSUPPORTED_PAGE,
            "The page is not a supported Glassdoor company page.",
            state=ConnectorState.UNSUPPORTED,
            details={"url": url},
        )
