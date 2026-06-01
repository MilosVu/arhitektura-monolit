import asyncio
import time
from datetime import UTC, datetime

import httpx
from cortex_core.celery_app import create_celery_app
from cortex_core.infrastructure.weaviate.client import ping_weaviate
from cortex_core.settings import get_settings
from cortex_models import get_engine
from module_ai.api import AiModule
from sqlalchemy import text

from module_platform.infrastructure.redis import ping_redis
from module_platform.schemas import ComponentStatus, SystemStatusResponse

settings = get_settings()
celery_app = create_celery_app("system_check")


async def _timed_check(name: str, check_fn) -> ComponentStatus:
    start = time.perf_counter()
    try:
        detail = (
            await check_fn() if asyncio.iscoroutinefunction(check_fn) else check_fn()
        )
        latency = (time.perf_counter() - start) * 1000
        if detail is True or detail == "ok":
            return ComponentStatus(name=name, status="ok", latency_ms=round(latency, 1))
        return ComponentStatus(
            name=name,
            status="degraded" if detail else "down",
            latency_ms=round(latency, 1),
            detail=str(detail) if detail not in (True, False, "ok") else None,
        )
    except Exception as exc:
        latency = (time.perf_counter() - start) * 1000
        return ComponentStatus(
            name=name,
            status="down",
            latency_ms=round(latency, 1),
            detail=str(exc),
        )


def _check_postgres() -> bool:
    with get_engine().connect() as conn:
        conn.execute(text("SELECT 1"))
    return True


def _check_redis() -> bool:
    return ping_redis()


def _check_weaviate() -> bool:
    return ping_weaviate()


async def _check_rabbitmq() -> bool:
    async with httpx.AsyncClient(timeout=3.0) as client:
        r = await client.get(
            f"{settings.rabbitmq_management_url.rstrip('/')}/api/overview",
            auth=("cortex", "cortex"),
        )
        return r.status_code == 200


def _check_celery() -> bool | str:
    inspect = celery_app.control.inspect(timeout=2.0)
    ping = inspect.ping()
    if ping:
        return True
    return "no workers responding"


async def get_system_status(ai_module: AiModule | None = None) -> SystemStatusResponse:
    ai = ai_module or AiModule()

    checks = await asyncio.gather(
        _timed_check("cortex-server", lambda: True),
        _timed_check("postgres", _check_postgres),
        _timed_check("redis", _check_redis),
        _timed_check("rabbitmq", _check_rabbitmq),
        _timed_check("weaviate", _check_weaviate),
        _timed_check("neo4j", ai.ping_neo4j),
        _timed_check("celery", _check_celery),
    )

    statuses = list(checks)
    down_count = sum(1 for c in statuses if c.status == "down")
    degraded_count = sum(1 for c in statuses if c.status == "degraded")

    if down_count > 0:
        overall = "down"
    elif degraded_count > 0:
        overall = "degraded"
    else:
        overall = "ok"

    return SystemStatusResponse(
        overall=overall,
        components=statuses,
        checked_at=datetime.now(UTC),
    )
