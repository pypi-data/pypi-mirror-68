from helpers.alert import AlertLabel, AlertSeverity, alert_object
from helpers import audatex_software, valid_audatex_version
from helpers.messages import (inspection_date_missing, not_locked_estimate,
                              not_valid_audatex_version, total_loss_estimate_alert,
                              vehicle_mileage_missing, wrong_header_alert)

# Compliance Checks


def wrong_header(ems) -> bool or object:
    if not _valid_header(ems.ins_co_name):
        return alert_object(
            AlertLabel.WRONG_HEADER.value,
            AlertSeverity.ERROR.value,
            lambda: wrong_header_alert()
        )

    return True


def locked_ems(ems, carrier_locked_ems) -> bool or object:
    if _locked_ems(ems.status):
        return True

    if carrier_locked_ems is True:
        return alert_object(
            AlertLabel.ESTIMATE_NOT_LOCKED.value,
            AlertSeverity.FAILURE.value,
            lambda: not_locked_estimate()
        )

    return True


def audatex_version(ems) -> bool or object:
    if audatex_software(ems) and valid_audatex_version(ems):
        return True

    return alert_object(
        AlertLabel.AUDATEX_VERSION.value,
        AlertSeverity.ERROR.value,
        lambda: not_valid_audatex_version()
    )


def inspection_date(ems) -> bool or object:
    if ems.insp_date:
        return True

    return alert_object(
        AlertLabel.INSPECTION_DATE_MISSING.value,
        AlertSeverity.WARNING.value,
        lambda: inspection_date_missing()
    )


def total_loss(ems) -> bool or object:
    if _valid_total_loss(ems.g_ttl_amt):
        return True

    return alert_object(
        AlertLabel.CONFIRM_ESTIMATE_TOTAL.value,
        AlertSeverity.WARNING.value,
        lambda: total_loss_estimate_alert(ems.g_ttl_amt)
    )


def vehicle_mileage(ems) -> bool or object:
    if _valid_vehicle_mileage(ems.v_mileage):
        return True

    return alert_object(
        AlertLabel.MILEAGE_MISSING.value,
        AlertSeverity.WARNING.value,
        lambda: vehicle_mileage_missing()
    )

# Internal Functions


def _valid_header(ems_header: str) -> bool:
    return ems_header not in _forbidden_firm_names()


def _forbidden_firm_names() -> list:
    return ['SCA', 'PDA', 'IANET', 'IA NET']


def _locked_ems(ems_status: str) -> bool:
    return ems_status in ('true', '1')


def _valid_inspection_date(insp_date: str or None) -> bool:
    return insp_date is not None and insp_date.lenght() > 1


def _valid_vehicle_mileage(mileage: int or None) -> bool:
    return mileage is not None and mileage > 0


def _valid_total_loss(total_loss_amt: int or None) -> bool:
    return total_loss_amt is not None and total_loss_amt > 0
