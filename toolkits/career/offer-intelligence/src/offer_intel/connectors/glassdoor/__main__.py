"""Run the local Glassdoor viability check.

Usage: ``python -m offer_intel.connectors.glassdoor``
"""

from __future__ import annotations

import asyncio

from .browser import check_viability


async def _main() -> None:
    report = await check_viability()
    print(report.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(_main())
