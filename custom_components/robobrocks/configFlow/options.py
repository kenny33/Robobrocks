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

        menu = ["pc_add", "pc_import"]
        if store.slots:
            menu += ["pc_rename", "pc_delete", "pc_restore"]

        return self.async_show_menu(
            step_id="permanent_codes",
            menu_options=menu,
            description_placeholders={
                "slots": "\n".join(lines) if lines else "-",
                "registry_count": str(len(lines)),
                "box_count": "?" if box_count is None else str(box_count),
            },
        )

    def _validate_new_slot(self, user_input: dict[str, Any], errors: dict, code_required: bool) -> str | None:
        """Common checks for adding/importing a slot. Return the normalized code."""
        store = self._coordinator.permanent_codes
        index = user_input["slot"] = int(user_input["slot"])
        if store.get(index) is not None:
            errors["slot"] = "slot_in_use"

        raw_code = user_input.get("code")
        if not raw_code and not code_required:
            return "".join(secrets.choice(ROBOBROCKS_CHAR_MAP) for _ in range(6))

        code = _normalize_code(raw_code)
        if code is None:
            errors["code"] = "invalid_code_format"
        elif store.find_code(code) is not None:
            errors["code"] = "code_in_use"
        return code

    def _new_slot_schema(self, user_input: dict[str, Any] | None, code_required: bool) -> vol.Schema:
        user_input = user_input or {}
        store = self._coordinator.permanent_codes
        code_key = vol.Required if code_required else vol.Optional
        return vol.Schema(
            {
                vol.Required("slot", default=str(user_input.get("slot", store.first_free()))): (
                    self._all_slots_selector()
                ),
                code_key("code", description={"suggested_value": user_input.get("code")}): str,
                vol.Optional("label", default=user_input.get("label", "")): str,
            }
        )

    async def async_step_pc_add(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Create a permanent code on the device and record it."""
        errors: dict[str, str] = {}
        placeholders = {"error": ""}

        if user_input is not None:
            code = self._validate_new_slot(user_input, errors, code_required=False)
            if not errors:
                index = user_input["slot"]
                try:
                    await self._coordinator.codes.create_code(code, "master", index)
                except HomeAssistantError as err:
                    _LOGGER.error("Could not create permanent code in slot %d: %s", index, err)
                    errors["base"] = "box_error"
                    placeholders["error"] = f"\n\n**{err}**"
                else:
                    await self._coordinator.permanent_codes.set_slot(index, code, user_input.get("label", ""))
                    await self._coordinator.async_request_refresh()
                    return self.async_abort(
                        reason="pc_added", description_placeholders={"slot": str(index), "code": code}
                    )

        return self.async_show_form(
            step_id="pc_add",
            data_schema=self._new_slot_schema(user_input, code_required=False),
            errors=errors,
            description_placeholders=placeholders,
        )

    async def async_step_pc_import(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Record a code that already exists on the device (nothing is sent)."""
        errors: dict[str, str] = {}

        if user_input is not None:
            code = self._validate_new_slot(user_input, errors, code_required=True)
            if not errors:
                index = user_input["slot"]
                await self._coordinator.permanent_codes.set_slot(index, code, user_input.get("label", ""))
                # Back to the list, so several codes can be imported in a row
                return await self.async_step_permanent_codes()

        return self.async_show_form(
            step_id="pc_import",
            data_schema=self._new_slot_schema(user_input, code_required=True),
            errors=errors,
        )

    async def async_step_pc_rename(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        """Change the label of a slot (the code itself is not touched)."""
        store = self._coordinator.permanent_codes
        if user_input is not None:
            await store.set_label(int(user_input["slot"]), user_input.get("label", ""))
            return await self.async_step_permanent_codes()

        return self.async_show_form(
            step_id="pc_rename",
            data_schema=vol.Schema(
                {
                    vol.Required("slot"): self._slot_selector(),
                    vol.Optional("label", default=""): str,
                }
            ),
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
