"""Base exception class for Robobrocks errors."""
from homeassistant.exceptions import HomeAssistantError

from ..const import DOMAIN


class RobobrocksError(HomeAssistantError):
    """Base class for Robobrocks errors."""
    def __init__(self, translation_key: str, translation_placeholders: dict[str, str] | None = None):
        super().__init__(
            translation_key,
            translation_domain=DOMAIN,
            translation_key=translation_key,
            translation_placeholders=translation_placeholders
        )
