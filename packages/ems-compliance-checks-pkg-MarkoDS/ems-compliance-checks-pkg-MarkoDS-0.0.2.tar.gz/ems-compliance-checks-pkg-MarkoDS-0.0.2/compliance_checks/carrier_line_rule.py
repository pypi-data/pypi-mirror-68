import datetime
import operator

import itertools

from helpers.alert import AlertSeverity, AlertLabel, alert_object
from helpers.compare import valid_part_type, present_math_operator
from helpers.line_rule_term import LINE_TERMS
from helpers.messages import construct_line_rule_message


def carrier_line_rule_check(line_rule, ems_lines, vehicle, ems):
    try:
        terms = LINE_TERMS[line_rule.line_rule]
    except KeyError:
        return None

    matching_lines = []
    for ems_line in ems_lines:
        if not valid_ems_line_description(terms, ems_line):
            if passed_checks(line_rule, ems_line, vehicle, ems):
                continue
            matching_lines.append(ems_line.line_no)
        continue

    return alert_object(
        AlertLabel.LINE_RULE_ERROR.value,
        AlertSeverity(line_rule.severity.upper()).value,
        lambda: construct_line_rule_message(line_rule, matching_lines)
    ) if len(matching_lines) > 0 else None


def passed_checks(line_rule, ems_line, vehicle, ems):
    checks = get_checks_by_line_rule_attrs(
        line_rule, ems_line, vehicle, ems
    )
    return len(checks) > 0 and any(check is True for check in checks)


def valid_ems_line_description(terms, ems_line):
    for term in terms:
        if all(t in ems_line.line_desc.lower() for t in term):
            return False
        continue

    return True


def valid_labor_type_code(line_rule, ems_line):
    if not _present_labor_type_code(ems_line):
        return True

    if ems_line.lbr_op == line_rule.labor_type_code:
        return False

    return True


def valid_labor_criteria(line_rule, ems_line):
    if not present_math_operator(line_rule.labor_operator):
        return True

    labor_type, labor_value = line_rule.labor_type, line_rule.labor_value
    ems_line_value = getattr(ems_line, labor_type)

    if not _present_labor_criteria(ems_line_value):
        return True

    # TO DO: REFACTOR

    if line_rule.labor_operator == '>':
        return False if ems_line_value > labor_value else True

    if line_rule.labor_operator == '>=':
        return False if ems_line_value >= labor_value else True

    if line_rule.labor_operator == '<':
        return False if ems_line_value < labor_value else True

    if line_rule.labor_operator == '=<':
        return False if ems_line_value <= labor_value else True

    if line_rule.labor_operator == '=':
        return False if ems_line_value == labor_value else True

    return True


def valid_vehicle_criteria(line_rule, vehicle):
    if not _valid_vehicle_year(vehicle):
        return True

    if line_rule.vehicle_year_condition == 'OLDER':
        return False if vehicle.year <= datetime.datetime.now().year - \
                        int(line_rule.vehicle_year_count) else True

    if line_rule.vehicle_year_condition == 'NEWER':
        return False if vehicle.year >= datetime.datetime.now().year - \
                        int(line_rule.vehicle_year_count) else True

    return True


def valid_mileage_criteria(line_rule, ems):
    if not present_math_operator(line_rule.mileage_operator):
        return True

    if not _valid_mileage_values(ems):
        return True

    if not _valid_mileage_values(ems):
        return True

    # TO DO: REFACTOR

    if line_rule.mileage_operator == '>':
        return False if ems.v_mileage > line_rule.mileage_amount else True

    if line_rule.mileage_operator == '>=':
        return False if ems.v_mileage >= line_rule.mileage_amount else True

    if line_rule.mileage_operator == '<':
        return False if ems.v_mileage < line_rule.mileage_amount else True

    if line_rule.mileage_operator == '=<':
        return False if ems.v_mileage <= line_rule.mileage_amount else True

    if line_rule.mileage_operator == '=':
        return False if ems.v_mileage == line_rule.mileage_amount else True


def valid_part_type_criteria(line_rule, ems_line):
    line_rule_lookup_types = _get_file_extension_by_part_type(line_rule)
    if ems_line.part_type not in line_rule_lookup_types:
        return True

    return False


def _present_labor_type_code(ems_line):
    if ems_line.lbr_op is None:
        return False

    return True


def _present_labor_criteria(ems_line_value):
    return ems_line_value is not None


def _present_vehicle_years(line_rule, vehicle):
    return line_rule.vehicle_year is not None and vehicle.year is not None


def _valid_vehicle_year(vehicle):
    return vehicle.year is not None


def _valid_mileage_values(ems):
    if ems.v_mileage is None:
        return False

    return True


def _valid_part_types(line_rule, ems_line):
    if ems_line.part_type is None:
        return False

    return valid_part_type(line_rule.part_types)


def _get_math_operator_by_string(math_operator: str, value1, value2):
    return {
        '>': lambda: operator.gt(value1, value2),
        '<': lambda: operator.lt(value1, value2),
        '=': lambda: operator.eq(value1, value2),
        '>=': lambda: operator.ge(value1, value2),
        '<=': lambda: operator.le(value1, value2)
    }[math_operator]


def _get_file_extension_by_part_type(line_rule):
    part_types = line_rule.part_types
    extensions = {
        'NEW': ['PAN'],
        'AFTERMARKET': ['PAA'],
        'USED': ['PAM', 'PAL']
    }

    if isinstance(part_types, list):
        return list(itertools.chain(
            *[extensions[part_type] for part_type in part_types]
        ))

    return extensions[part_types]


def get_checks_by_line_rule_attrs(line_rule, ems_line, vehicle, ems):
    mapping = check_mappings(line_rule, ems_line, vehicle, ems)
    line_rule_attrs = [
        attr for attr in (list(mapping.keys()))
        if valid_value(line_rule, attr)
    ]

    return [mapping[attrs]() for attrs in line_rule_attrs]


def check_mappings(line_rule, ems_line, vehicle, ems):
    return {
        ('labor_type_code', ):
            lambda: valid_labor_type_code(line_rule, ems_line),
        ('labor_operator', 'labor_type', 'labor_value'):
            lambda: valid_labor_criteria(line_rule, ems_line),
        ('vehicle_year_count', 'vehicle_year_condition'):
            lambda: valid_vehicle_criteria(line_rule, vehicle),
        ('mileage_operator', 'mileage_amount'):
            lambda: valid_mileage_criteria(line_rule, ems),
        ('part_types', ):
            lambda: valid_part_type_criteria(line_rule, ems_line)
    }


def valid_value(line_rule, attrs):
    valid = False
    for attr in attrs:
        valid = _valid_value(getattr(line_rule, attr))

    return valid


def _valid_value(value):
    if value is None:
        return False

    if type(value) is str:
        return len(value) > 0

    return True
