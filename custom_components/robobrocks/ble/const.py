"""Constants for Robobrocks BLE communication."""
from enum import IntEnum, StrEnum


class RobobrocksServiceUUID(StrEnum):
    """UUIDs for Robobrocks services and characteristics."""
    SERVICE = "a7630001-f491-4f21-95ea-846ba586e361"
    WRITE_CHARACTERISTIC = "a7630002-f491-4f21-95ea-846ba586e361"
    NOTIFY_CHARACTERISTIC = "a7630003-f491-4f21-95ea-846ba586e361"
    BATTERY_CHARACTERISTIC = "00000004-0000-1000-8000-00805f9b34fb"

    BATTERY_SERVICE = "0000180f-0000-1000-8000-00805f9b34fb"
    BATTERY_LEVEL_CHARACTERISTIC = "00002a19-0000-1000-8000-00805f9b34fb"

    DEVICE_INFO_SERVICE = "0000180a-0000-1000-8000-00805f9b34fb"
    SYSTEM_ID_CHARACTERISTIC = "00002a23-0000-1000-8000-00805f9b34fb"
    MODEL_NUMBER_CHARACTERISTIC = "00002a24-0000-1000-8000-00805f9b34fb"
    SERIAL_NUMBER_CHARACTERISTIC = "00002a25-0000-1000-8000-00805f9b34fb"
    INTERNAL_FIRMWARE_REVISION_CHARACTERISTIC = "00002a26-0000-1000-8000-00805f9b34fb"
    HARDWARE_REVISION_CHARACTERISTIC = "00002a27-0000-1000-8000-00805f9b34fb"
    SOFTWARE_REVISION_CHARACTERISTIC = "00002a28-0000-1000-8000-00805f9b34fb"
    MANUFACTURER_NAME_CHARACTERISTIC = "00002a29-0000-1000-8000-00805f9b34fb"

class RobobrocksCommandOpcode(IntEnum):
    """Opcodes for commands sent to the Robobrocks (Downlink)."""
    OPEN_DOOR = 0x01
    ASK_DOOR_STATUS = 0x02
    REQUEST_LOGS = 0x03
    REBOOT = 0x06
    GET_LOGS_COUNT = 0x07
    TEST_BATTERY = 0x08
    MASTER_CODE_EDIT = 0x09
    SINGLE_USE_CODE_TO_MULTI = 0x0A
    MULTI_CODE_TO_SINGLE_USE = 0x0B
    DELETE_MASTER_CODE = 0x0C
    DELETE_SINGLE_USE_CODE = 0x0D
    DELETE_MULTI_USE_CODE = 0x0E
    REACTIVATE_CODE = 0x0F
    GENERATE_CODES = 0x10
    CREATE_MASTER_CODE = 0x11
    CREATE_SINGLE_USE_CODE = 0x12
    CREATE_MULTI_USE_CODE = 0x13
    COUNT_CODES = 0x14
    GENERATE_CODES_SUPPORT = 0x15
    SET_CONFIGURATION = 0x16
    REGISTER_NFC_TAG_SCAN_START = 0x17
    REGISTER_NFC_TAG = 0x18
    UNREGISTER_NFC_TAG = 0x19

class RobobrocksNotificationOpcode(IntEnum):
    """Opcodes for notifications received from the Robobrocks (Uplink)."""
    CODE_OPERATION_SUCCESS = 0x77
    CODE_OPERATION_ERROR = 0x78
    NOTIFY_LOGS_COUNT = 0x79
    ERROR_COMMAND_NOT_SUPPORTED = 0x80
    VALID_OPEN_CODE = 0x81
    INVALID_OPEN_CODE = 0x82
    NOTIFY_DOOR_STATUS = 0x84
    ANSWER_DOOR_STATUS = 0x85
    NOTIFY_CODE_GENERATION_SUCCESS = 0xC0
    NOTIFY_CODE_GENERATION_ERROR = 0xC1
    NOTIFY_CODES_COUNT = 0xC3
    NOTIFY_SET_CONFIGURATION_SUCCESS = 0xC4
    NOTIFY_NFC_TAG_FOUND = 0xC5
    ERROR_NFC_TAG_ALREADY_EXISTS_SCAN = 0xC6
    ERROR_NFC_SCAN_TIMEOUT = 0xC7
    NOTIFY_NFC_TAG_REGISTERED = 0xC8
    ERROR_NFC_TAG_ALREADY_EXISTS_REGISTER = 0xC9
    NOTIFY_NFC_TAG_UNREGISTERED = 0xCA
    ERROR_CRC = 0xE0
    ERROR_UNAUTHORIZED = 0xE1
    ERROR_BAD_REQUEST = 0xE2

class RobobrocksHistoryEvent(IntEnum):
    """Opcodes for history events (logs)."""
    CODE_BLE_VALID = 0x86
    CODE_KEY_VALID = 0x87
    CODE_BLE_INVALID = 0x88
    CODE_KEY_INVALID = 0x89
    DOOR_CLOSED = 0x90
    DOOR_OPENED = 0x91
    LOG_END_HISTORY = 0x92
    HISTORY_ERASE = 0x93
    POWER_OFF = 0x94
    BLOCK_RESET = 0x95
    POWER_ON = 0x96
    BLE_REBOOT = 0x97
    SCALE_CONTINUOUS_MEASURE = 0x98
    KEY_OPENING = 0x99
    ERROR = 0xA0
    NFC_OPENING = 0xA1
    NFC_TAG_REGISTERING_SCAN = 0xA2

class RobobrocksPowerOffReason(IntEnum):
    """Reason codes for POWER_OFF event."""
    PIN_RESET = 1
    WATCHDOG = 2
    SOFT_RESET = 3
    LOCKUP = 4
    POWER_ON = 5
    WAKEUP_NFC = 6
    WAKEUP_SYSTEM_OFF = 7
    WAKEUP_LPCOMP = 8

class RobobrocksDiagnosticErrorCode(IntEnum):
    """Specific error codes for diagnostic events (0xA0)."""
    MFRC630_ERROR_BC = 0xBC
    MFRC630_ERROR_INTEGRITY = 0x13
    MFRC630_ERROR_NO_TAG = 0x15
    MFRC630_ERROR_COLLISION = 0x0B
    MFRC630_ERROR_BUFFER = 0x03

ERROR_DESCRIPTIONS = {
    RobobrocksDiagnosticErrorCode.MFRC630_ERROR_BC: "diagnostic_error_bc",
    RobobrocksDiagnosticErrorCode.MFRC630_ERROR_INTEGRITY: "diagnostic_error_integrity",
    RobobrocksDiagnosticErrorCode.MFRC630_ERROR_NO_TAG: "diagnostic_error_no_tag",
    RobobrocksDiagnosticErrorCode.MFRC630_ERROR_COLLISION: "diagnostic_error_collision",
    RobobrocksDiagnosticErrorCode.MFRC630_ERROR_BUFFER: "diagnostic_error_buffer",
    "UNKNOWN_ERROR": "diagnostic_error_unknown",
}

LOG_EVENT_DESCRIPTIONS = {
    RobobrocksHistoryEvent.CODE_BLE_VALID: "code_ble_valid",
    RobobrocksHistoryEvent.CODE_KEY_VALID: "code_key_valid",
    RobobrocksHistoryEvent.CODE_BLE_INVALID: "code_ble_invalid",
    RobobrocksHistoryEvent.CODE_KEY_INVALID: "code_key_invalid",
    RobobrocksHistoryEvent.DOOR_CLOSED: "door_closed",
    RobobrocksHistoryEvent.DOOR_OPENED: "door_opened",
    RobobrocksHistoryEvent.HISTORY_ERASE: "history_erase",
    RobobrocksHistoryEvent.POWER_OFF: "power_off",
    RobobrocksHistoryEvent.BLOCK_RESET: "block_reset",
    RobobrocksHistoryEvent.POWER_ON: "power_on",
    RobobrocksHistoryEvent.BLE_REBOOT: "ble_reboot",
    RobobrocksHistoryEvent.SCALE_CONTINUOUS_MEASURE: "scale_measure",
    RobobrocksHistoryEvent.KEY_OPENING: "key_opening",
    RobobrocksHistoryEvent.ERROR: "error",
    RobobrocksHistoryEvent.NFC_OPENING: "nfc_opening",
    RobobrocksHistoryEvent.NFC_TAG_REGISTERING_SCAN: "nfc_tag_registering_scan",
}

LOG_EVENT_TYPES = {
    RobobrocksHistoryEvent.CODE_BLE_VALID: "code_ble_valid",
    RobobrocksHistoryEvent.CODE_KEY_VALID: "code_key_valid",
    RobobrocksHistoryEvent.CODE_BLE_INVALID: "code_ble_invalid",
    RobobrocksHistoryEvent.CODE_KEY_INVALID: "code_key_invalid",
    RobobrocksHistoryEvent.DOOR_CLOSED: "door_closed",
    RobobrocksHistoryEvent.DOOR_OPENED: "door_opened",
    RobobrocksHistoryEvent.HISTORY_ERASE: "history_erase",
    RobobrocksHistoryEvent.POWER_OFF: "power_off",
    RobobrocksHistoryEvent.BLOCK_RESET: "block_reset",
    RobobrocksHistoryEvent.POWER_ON: "power_on",
    RobobrocksHistoryEvent.BLE_REBOOT: "ble_reboot",
    RobobrocksHistoryEvent.SCALE_CONTINUOUS_MEASURE: "scale_measure",
    RobobrocksHistoryEvent.KEY_OPENING: "key_opening",
    RobobrocksHistoryEvent.ERROR: "error",
    RobobrocksHistoryEvent.NFC_OPENING: "nfc_opening",
    RobobrocksHistoryEvent.NFC_TAG_REGISTERING_SCAN: "nfc_tag_registering_scan",
}

class RobobrocksCodeType(StrEnum):
    """Code types for Robobrocks."""
    MASTER = "master"
    SINGLE_USE = "single_use"
    MULTI_USE = "multi_use"

class RobobrocksConfigType(IntEnum):
    """Configuration types for Robobrocks (SET_CONFIGURATION)."""
    SCAN_LAPOSTE_NFC_TAGS = 0x01

class RobobrocksNfcTagType(IntEnum):
    """NFC Tag types for Robobrocks."""
    LA_POSTE = 0x01
    VIGIK_TERTIARY = 0x02
    USER_BADGE = 0x03
