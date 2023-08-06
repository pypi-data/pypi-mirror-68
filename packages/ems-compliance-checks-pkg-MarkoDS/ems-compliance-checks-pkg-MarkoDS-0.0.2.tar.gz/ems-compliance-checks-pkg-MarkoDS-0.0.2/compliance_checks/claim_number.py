from helpers.alert import AlertLabel, AlertSeverity, alert_object
from helpers import matching_floats, matching_strings
from helpers.messages import (missing_claim_number, not_matching_claim_number,
                              not_matching_deductible)


def match_claim_number(claim, ems) -> bool or object:
    claim_number, ems_claim_number = claim.claim_number, ems.clm_no
    if not matching_strings(claim_number, ems_claim_number):
        return alert_object(
            AlertLabel.WRONG_CLAIM_NUMBER.value,
            AlertSeverity.WARNING.value,
            lambda: not_matching_claim_number(ems_claim_number)
        )

    return True


def ems_with_claim_number(ems) -> bool or object:
    if ems.clm_no is None:
        return alert_object(
            AlertLabel.CLAIM_NUMBER_MISSING.value,
            AlertSeverity.WARNING.value,
            lambda: missing_claim_number()
        )

    return True


def match_deductible(claim, ems):
    claim_deductible, ems_deductible = _deductible_value(claim.deductible), \
                                       _deductible_value(ems.g_ded_amt)

    if not matching_floats(claim_deductible, ems_deductible):
        return alert_object(
            AlertLabel.WRONG_DEDUCTIBLE.value,
            AlertSeverity.ERROR.value,
            lambda: not_matching_deductible(claim_deductible, ems_deductible)
        )

    return True


def _deductible_value(deductible: int or None) -> float:
    return deductible if deductible else 0.00
