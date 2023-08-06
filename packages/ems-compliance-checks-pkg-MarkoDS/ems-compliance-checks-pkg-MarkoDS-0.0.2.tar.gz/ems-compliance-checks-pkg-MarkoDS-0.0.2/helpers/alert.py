from enum import Enum
from typing import Callable


def alert_object(label: str, severity: str, message_func: Callable) -> object:
    return Alert(label, severity, message_func())


class Alert:
    def __init__(self, label, severity, message):
        self.alert = label
        self.type = severity
        self.message = message


class AlertSeverity(Enum):
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    FAILURE = 'FAILURE'


class AlertLabel(Enum):
    WRONG_CLAIM_NUMBER = 'WRONG_CLAIM_NUMBER'
    CLAIM_NUMBER_MISSING = 'CLAIM_NUMBER_MISSING'
    WRONG_DEDUCTIBLE = 'WRONG_DEDUCTIBLE'
    WRONG_HEADER = 'WRONG_HEADER'
    ESTIMATE_NOT_LOCKED = 'ESTIMATE_NOT_LOCKED'
    AUDATEX_VERSION = 'AUDATEX_VERSION'
    INSPECTION_DATE_MISSING = 'INSPECTION_DATE_MISSING'
    CONFIRM_ESTIMATE_TOTAL = 'CONFIRM_ESTIMATE_TOTAL'
    MILEAGE_MISSING = 'MILEAGE_MISSING'
    EMS_REQUIRED_EXTENSION = 'EMS_REQUIRED_EXTENSION'
    LINE_RULE_ERROR = 'LINE_RULE_ERROR'
