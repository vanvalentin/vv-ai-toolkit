"""Run the MCP gateway over stdio."""

from __future__ import annotations

import logging
import sys

from .server import create_mcp_server


def main() -> None:
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.WARNING,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    create_mcp_server().run(transport="stdio", show_banner=False)


if __name__ == "__main__":
    main()
