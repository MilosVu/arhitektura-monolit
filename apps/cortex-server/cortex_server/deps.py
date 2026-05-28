"""Re-export auth deps for cortex-server composition root."""

from module_platform.deps import get_current_user

__all__ = ["get_current_user"]
