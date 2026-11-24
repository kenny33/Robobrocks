"""Error classes for Robobrocks."""
from .robobrocks_auth_error import RobobrocksAuthError
from .robobrocks_command_error import RobobrocksCommandError
from .robobrocks_error import RobobrocksError

__all__ = [
    "RobobrocksError",
    "RobobrocksAuthError",
    "RobobrocksCommandError",
]
