from contextvars import ContextVar
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi_metabot.models import CommandMetadata, ActionMetadata  # noqa
    from fastapi_metabot.module import Module  # noqa


command_metadata: ContextVar[Optional['CommandMetadata']] = ContextVar(
    'command_metadata',
    default=None
)

action_metadata: ContextVar[Optional['ActionMetadata']] = ContextVar(
    'action_metadata',
    default=None
)

current_module: ContextVar[Optional['Module']] = ContextVar(
    'current_module',
    default=None
)
