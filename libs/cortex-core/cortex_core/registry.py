"""Typed service container za dependency injection."""

from __future__ import annotations

from cortex_core.errors import ServiceNotRegisteredError


class ServiceRegistry:
    """Typed kontejner servisa — puni se u composition root-u pri startu."""

    def __init__(self) -> None:
        self._services: dict[type, object] = {}

    def register[T](self, service_type: type[T], instance: T) -> None:
        if service_type in self._services:
            msg = f"{service_type.__name__} već registrovan"
            raise ValueError(msg)
        self._services[service_type] = instance

    def resolve[T](self, service_type: type[T]) -> T:
        if (instance := self._services.get(service_type)) is not None:
            return instance  # type: ignore[return-value]
        msg = (
            f"{service_type.__name__} nije registrovan"
            " — pozovi register_services() pri startu"
        )
        raise ServiceNotRegisteredError(msg)

    def is_registered(self, service_type: type) -> bool:
        return service_type in self._services

    def reset(self) -> None:
        self._services.clear()
