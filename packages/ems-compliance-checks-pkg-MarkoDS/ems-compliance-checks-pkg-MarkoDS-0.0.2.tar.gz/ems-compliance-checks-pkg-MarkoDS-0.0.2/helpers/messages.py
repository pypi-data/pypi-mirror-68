def not_matching_claim_number(number):
    """Return message for not matching claim number alert."""
    return (
            "CLAIM NUMBER DOESN'T MATCH: CLAIM NUMBER " +
            "ON ESTIMATE MUST MATCH CLIENT CLAIM NUMBER: "
            "{} -- PLEASE REVISE.".format(number)
    )


def missing_claim_number():
    """Return message for missing claim number."""
    return (
        "CLAIM NUMBER MUST BE ON YOUR ESTIMATE, PLEASE REVISE."
    )


def not_matching_deductible(claim_deductible, ems_deductible):
    """Return message for not matching deductible."""
    return (
            "DEDUCTIBLE DOESN'T MATCH: "
            "DEDUCTIBLE ON ESTIMATE (${}) ".format(ems_deductible) +
            "DOESN'T MATCH THE DEDUCTIBLE FROM " +
            "CLIENT: ${} -- PLEASE REVISE.".format(claim_deductible)
    )


def wrong_header_alert():
    """Return message fro wrong header alert."""
    return (
            "ACD MUST BE ON THE HEADER AND IN THE ESTIMATE. " +
            "PLEASE REMOVE THE OTHER FIRM\'S NAME."
    )


def not_locked_estimate():
    """Return message for unlocked ems."""
    return (
            "ESTIMATE NOT LOCKED: THE CLIENT " +
            "REQUIRES ESTIMATES TO BE LOCKED -- PLEASE REVISE AND RE-UPLOAD."
    )


def not_valid_audatex_version():
    """Return message for invalid audatex version."""
    return (
        "YOU MUST USE AUDATEX EMS VERSION 2.6 OR HIGHER."
    )


def inspection_date_missing():
    """Return message for missing inspection date."""
    return (
        "INSPECTION DATE MUST BE ON YOUR ESTIMATE, PLEASE REVISE."
    )


def total_loss_estimate_alert(g_ttl_amt):
    """Return message for total loss estimates."""
    return (
            "TOTAL EST AMOUNT: {} - THIS IS JUST TO ".format(g_ttl_amt) +
            "CONFIRM THE TOTAL ESTIMATE AMOUNT FROM YOUR EMS FILES. " +
            "IF THIS IS NOT CORRECT RE-UPLOAD THE LATEST EMS FILES."
    )


def vehicle_mileage_missing():
    """Return message for missing mileage."""
    return (
            "MILEAGE MISSING: MILEAGE IS NOT ON YOUR ESTIMATE. " +
            "ONLY EXCLUDE MILEAGE IF IT IS NOT AVAILABLE."
    )


def est_required_extension(extension):
    """Return message for missing required extension."""
    return (
        "YOU MUST UPLOAD AN ESTIMATE FILE OF TYPE: {}.".format(extension)
    )


def construct_line_rule_message(line_rule, lines: list) -> str:
    lines = str(lines).strip('[]')
    return f'{line_rule.line_rule}: ' \
           f'{line_rule.message}.[Matching Lines: {lines}]'
