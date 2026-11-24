import logging
import secrets
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from ..const import (
    CONF_ANONYMIZE_LOGS,
    CONF_MASTER_CODE,
    DEFAULT_FULL_REFRESH_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    ROBOBROCKS_CHAR_MAP,
)

_LOGGER = logging.getLogger(__name__)

MAX_SLOT = 255
SLOT_LIST_MIN_SIZE = 20


def _normalize_code(code: str | None) -> str | None:
    """Return the code upper-cased, or None if it is not a valid PIN."""
    code = (code or "").strip().upper()
    if len(code) == 6 and all(c in ROBOBROCKS_CHAR_MAP for c in code):
        return code
    return None


class RobobrocksOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Robobrocks options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.entry = config_entry
        self._edit_slot = 0

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Show the options menu."""
        return self.async_show_menu(step_id="init", menu_options=["settings", "permanent_codes"])

    async def async_step_settings(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Manage the options."""
        errors = {}

        if user_input is not None:
            # Validate and normalize Master Code if provided
            if user_input.get(CONF_MASTER_CODE):
                code = user_input[CONF_MASTER_CODE].strip().upper()
                if not (len(code) == 6 and all(c in ROBOBROCKS_CHAR_MAP for c in code)):
                    errors[CONF_MASTER_CODE] = "invalid_master_code_format"
                else:
                    user_input[CONF_MASTER_CODE] = code

            if not errors:
                return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="settings",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "scan_interval",
                        default=self.entry.options.get("scan_interval", DEFAULT_SCAN_INTERVAL),
                    ): int,
                    vol.Optional(
                        "full_refresh_interval",
                        default=self.entry.options.get("full_refresh_interval", DEFAULT_FULL_REFRESH_INTERVAL),
                    ): int,
                    vol.Optional(
                        CONF_MASTER_CODE,
                        description={"suggested_value": self.entry.options.get(CONF_MASTER_CODE)},
                    ): str,
                    vol.Optional(
                        CONF_ANONYMIZE_LOGS,
                        default=self.entry.options.get(CONF_ANONYMIZE_LOGS, False),
                    ): bool,
                }
            ),
            errors=errors,
        )

    # ------------------------------------------------------------------
    # Permanent codes (slot registry)
    # ------------------------------------------------------------------

    @property
    def _coordinator(self):
        return self.hass.data.get(DOMAIN, {}).get(self.entry.entry_id)

    def _slot_options(self) -> list[SelectOptionDict]:
        return [
            SelectOptionDict(value=str(index), label=f"{index} - {slot['label'] or '?'} ({slot['code']})")
            for index, slot in self._coordinator.permanent_codes.slots.items()
        ]

    def _all_slots_selector(self) -> SelectSelector:
        """Dropdown of slots 0..N showing, for each, the recorded code or that it is free."""
        store = self._coordinator.permanent_codes
        french = (self.hass.config.language or "").startswith("fr")
        free_txt = "libre" if french else "free"
        last = min(MAX_SLOT, max([SLOT_LIST_MIN_SIZE - 1, *[i + 5 for i in store.slots]]))
        options = []
        for index in range(last + 1):
            slot = store.get(index)
            if slot is None:
                label = f"{index} - {free_txt}"
            else:
                label = f"{index} - {slot['label'] or '?'} ({slot['code']})"
            options.append(SelectOptionDict(value=str(index), label=label))
        return SelectSelector(SelectSelectorConfig(options=options, mode=SelectSelectorMode.DROPDOWN))

    def _slot_selector(self) -> SelectSelector:
        return SelectSelector(
            SelectSelectorConfig(options=self._slot_options(), mode=SelectSelectorMode.DROPDOWN)
        )

    async def async_step_permanent_codes(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Show the permanent codes registry and its actions."""
        coordinator = self._coordinator
        if coordinator is None:
            return self.async_abort(reason="not_loaded")

        store = coordinator.permanent_codes
        lines = [
            f"- {index} : **{slot['code']}** {slot['label']}"
            + (f" ({slot['last_used'][:16].replace('T', ' ')})" if slot.get("last_used") else "")
            for index, slot in store.slots.items()
        ]
        box_count = (coordinator.data or {}).get("master")

        menu = ["pc_edit"]
        if store.slots:
            menu += ["pc_delete", "pc_restore"]

        return self.async_show_menu(
            step_id="permanent_codes",
            menu_options=menu,
            description_placeholders={
                "slots": "\n".join(lines) if lines else "-",
                "registry_count": str(len(lines)),
                "box_count": "?" if box_count is None else str(box_count),
            },
        )

    def _random_code(self) -> str:
        store = self._coordinator.permanent_codes
        while True:
            code = "".join(secrets.choice(ROBOBROCKS_CHAR_MAP) for _ in range(6))
            if store.find_code(code) is None:
                return code

    async def async_step_pc_edit(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Pick a slot (free or recorded) to create or modify."""
        if user_input is not None:
            self._edit_slot = int(user_input["slot"])
            return await self.async_step_pc_slot()

        store = self._coordinator.permanent_codes
        return self.async_show_form(
            step_id="pc_edit",
            data_schema=vol.Schema(
                {vol.Required("slot", default=str(store.first_free())): self._all_slots_selector()}
            ),
        )

    async def async_step_pc_slot(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Create or modify one slot, pre-filled with what is recorded."""
        store = self._coordinator.permanent_codes
        index = self._edit_slot
        current = store.get(index)
        errors: dict[str, str] = {}
        placeholders = {"slot": str(index), "error": ""}

        if user_input is not None:
            write = user_input.get("write_to_box", True)
            label = user_input.get("label", "")
            raw_code = user_input.get("code")
            if not raw_code and write:
                code = self._random_code()
            else:
                code = _normalize_code(raw_code)
                if code is None:
                    errors["code"] = "invalid_code_format"
                elif store.find_code(code) not in (None, index):
                    errors["code"] = "code_in_use"

            if not errors:
                if current is not None and code == current["code"]:
                    # Same code: only the label changes, nothing to send
                    await store.set_label(index, label)
                    return await self.async_step_permanent_codes()

                if write:
                    try:
                        await self._coordinator.codes.create_code(code, "master", index)
                    except HomeAssistantError as err:
                        _LOGGER.error("Could not write permanent code in slot %d: %s", index, err)
                        errors["base"] = "box_error"
                        placeholders["error"] = f"\n\n**{err}**"

                if not errors:
                    await store.set_slot(index, code, label)
                    if write:
                        await self._coordinator.async_request_refresh()
                    return await self.async_step_permanent_codes()

        defaults = user_input or {
            "code": current["code"] if current else None,
            "label": current["label"] if current else "",
            "write_to_box": True,
        }
        return self.async_show_form(
            step_id="pc_slot",
            data_schema=vol.Schema(
                {
                    vol.Optional("code", description={"suggested_value": defaults.get("code")}): str,
                    vol.Optional("label", default=defaults.get("label", "")): str,
                    vol.Optional("write_to_box", default=defaults.get("write_to_box", True)): bool,
                }
            ),
            errors=errors,
            description_placeholders=placeholders,
        )

    async def async_step_pc_delete(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Delete a slot from the device and/or from the registry."""
        errors: dict[str, str] = {}
        placeholders = {"error": ""}
        store = self._coordinator.permanent_codes

        if user_input is not None:
            index = int(user_input["slot"])
            if user_input.get("delete_on_box", True):
                try:
                    await self._coordinator.codes.delete_code("master", index)
                except HomeAssistantError as err:
                    _LOGGER.error("Could not delete permanent code in slot %d: %s", index, err)
                    errors["base"] = "box_error"
                    placeholders["error"] = f"\n\n**{err}**"
            if not errors:
                await store.remove_slot(index)
                await self._coordinator.async_request_refresh()
                return self.async_abort(reason="pc_deleted", description_placeholders={"slot": str(index)})

        return self.async_show_form(
            step_id="pc_delete",
            data_schema=vol.Schema(
                {
                    vol.Required("slot"): self._slot_selector(),
                    vol.Optional("delete_on_box", default=True): bool,
                }
            ),
            errors=errors,
            description_placeholders=placeholders,
        )

    async def async_step_pc_restore(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Write every registered slot back to the device."""
        store = self._coordinator.permanent_codes

        if user_input is not None:
            failed = []
            for index, slot in store.slots.items():
                try:
                    await self._coordinator.codes.create_code(slot["code"], "master", index)
                except HomeAssistantError as err:
                    _LOGGER.error("Could not restore permanent code in slot %d: %s", index, err)
                    failed.append(str(index))
            await self._coordinator.async_request_refresh()
            return self.async_abort(
                reason="pc_restored",
                description_placeholders={
                    "ok": str(len(store.slots) - len(failed)),
                    "failed": ", ".join(failed) if failed else "-",
                },
            )

        return self.async_show_form(
            step_id="pc_restore",
            data_schema=vol.Schema({}),
            description_placeholders={"count": str(len(store.slots))},
        )
