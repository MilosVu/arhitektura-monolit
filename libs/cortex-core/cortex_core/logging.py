"""Strukturirano logovanje za API i worker."""

from __future__ import annotations

import logging
import sys

_NOISY_LOGGERS = (
    "httpx",
    "httpcore",
    "sqlalchemy.engine",
    "urllib3",
    "celery",
    "kombu",
    "amqp",
)


class _HealthCheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "/health" not in record.getMessage()


def setup_logging(*, level: int = logging.INFO) -> None:
    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)-8s %(name)s — %(message)s")
    )
    root.addHandler(handler)

    for name in _NOISY_LOGGERS:
        logging.getLogger(name).setLevel(logging.WARNING)

    logging.getLogger("uvicorn.access").addFilter(_HealthCheckFilter())
