from urllib.parse import urlparse

import weaviate

from cortex_core.settings import get_settings

_client: weaviate.WeaviateClient | None = None


def get_weaviate_client() -> weaviate.WeaviateClient:
    global _client
    if _client is None:
        parsed = urlparse(get_settings().weaviate_url)
        host = parsed.hostname or "localhost"
        port = parsed.port or 8080
        _client = weaviate.connect_to_custom(
            http_host=host,
            http_port=port,
            http_secure=False,
            grpc_host=host,
            grpc_port=50051,
            grpc_secure=False,
            skip_init_checks=True,
        )
    return _client


def ping_weaviate() -> bool:
    try:
        return get_weaviate_client().is_ready()
    except Exception:
        return False
