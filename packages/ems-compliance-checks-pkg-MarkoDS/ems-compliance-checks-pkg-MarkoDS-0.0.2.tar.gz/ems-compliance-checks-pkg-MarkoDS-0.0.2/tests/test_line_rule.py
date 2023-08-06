import unittest

from compliance_checks.carrier_line_rule import carrier_line_rule_check, \
    valid_ems_line_description, valid_labor_type_code, valid_labor_criteria, \
    valid_vehicle_criteria, valid_mileage_criteria, valid_part_type_criteria
from helpers.line_rule_term import LINE_TERMS


class TestEmsWithLineErrors(unittest.TestCase):
    def test_carrier_line_rules(self):
        assert "BUMPER terms in line_desc" in carrier_line_rule_check(
            LineRule(line_rule="BUMPER", message="BUMPER terms in line_desc"),
            [EmsLine(line_desc="Frt Bumper Face Bar", line_no=1)],
            Vehicle(),
            Ems()
        ).message

    def test_none_1(self):
        assert carrier_line_rule_check(
            LineRule(line_rule="BUMPER", message="BUMPER terms in line_desc"),
            [EmsLine(line_desc="Frt Bumper", line_no=1)],
            Vehicle(),
            Ems()
        ) is None

    def test_message_1(self):
        assert "BUMPER terms in line_desc" in carrier_line_rule_check(
            LineRule(line_rule="BUMPER", message="BUMPER terms in line_desc",
                     labor_type_code='OP21'),
            [EmsLine(line_desc="Frt Bumper Face Bar", line_no=1,
                     lbr_op='OP21')],
            Vehicle(),
            Ems()
        ).message

    def test_none_2(self):
        assert carrier_line_rule_check(
            LineRule(line_rule="BUMPER", message="BUMPER terms in line_desc",
                     labor_type_code='OP21'),
            [EmsLine(line_desc="Frt Bumper Face Bar", line_no=1,
                     lbr_op='OP20')],
            Vehicle(),
            Ems()
        ) is None

    def test_message_2(self):
        assert "BUMPER terms in line_desc" in carrier_line_rule_check(
            LineRule(
                line_rule="BUMPER", message="BUMPER terms in line_desc",
                labor_type_code='OP21', labor_type="mod_lb_hrs",
                labor_operator='>', labor_value=100
            ),
            [EmsLine(line_desc="Frt Bumper Face Bar", line_no=1,
                     lbr_op='OP21', mod_lb_hrs=1500)],
            Vehicle(),
            Ems()
        ).message

    def test_none_3(self):
        assert carrier_line_rule_check(
            LineRule(
                line_rule="BUMPER", message="BUMPER terms in line_desc",
                labor_type_code='OP21', labor_type="mod_lb_hrs",
                labor_operator='<', labor_value=100
            ),
            [EmsLine(line_desc="Frt Bumper Face Bar", line_no=1,
                     lbr_op='OP21', mod_lb_hrs=1500)],
            Vehicle(),
            Ems()
        ) is None

    def test_message_3(self):
        assert "BUMPER terms in line_desc" in carrier_line_rule_check(
            LineRule(
                line_rule="BUMPER", message="BUMPER terms in line_desc",
                labor_type_code='OP21', labor_type="mod_lb_hrs",
                labor_operator='>', labor_value=100,
                vehicle_year_condition="OLDER", vehicle_year_count=10
            ),
            [EmsLine(line_desc="Frt Bumper Face Bar", line_no=1,
                     lbr_op='OP21', mod_lb_hrs=1500)],
            Vehicle(year=2000),
            Ems()
        ).message

    def test_none_4(self):
        assert carrier_line_rule_check(
            LineRule(
                line_rule="BUMPER", message="BUMPER terms in line_desc",
                labor_type_code='OP21', labor_type="mod_lb_hrs",
                labor_operator='>', labor_value=100,
                vehicle_year_condition="NEWER", vehicle_year_count=10
            ),
            [EmsLine(line_desc="Frt Bumper Face Bar", line_no=1,
                     lbr_op='OP21', mod_lb_hrs=1500)],
            Vehicle(year=2000),
            Ems()
        ) is None

    def test_message_4(self):
        assert "BUMPER terms in line_desc" in carrier_line_rule_check(
            LineRule(
                line_rule="BUMPER", message="BUMPER terms in line_desc",
                labor_type_code='OP21', labor_type="mod_lb_hrs",
                labor_operator='>', labor_value=100,
                vehicle_year_condition="OLDER", vehicle_year_count=10,
                mileage_operator=">", mileage_amount=100
            ),
            [EmsLine(line_desc="Frt Bumper Face Bar", line_no=1,
                     lbr_op='OP21', mod_lb_hrs=1500)],
            Vehicle(year=2000),
            Ems(v_mileage=200)
        ).message

    def test_none_5(self):
        assert carrier_line_rule_check(
            LineRule(
                line_rule="BUMPER", message="BUMPER terms in line_desc",
                labor_type_code='OP21', labor_type="mod_lb_hrs",
                labor_operator='>', labor_value=100,
                vehicle_year_condition="OLDER", vehicle_year_count=10,
                mileage_operator="<", mileage_amount=100
            ),
            [EmsLine(line_desc="Frt Bumper Face Bar", line_no=1,
                     lbr_op='OP21', mod_lb_hrs=1500)],
            Vehicle(year=2000),
            Ems(v_mileage=200)
        ) is None

    def test_message_5(self):
        assert "BUMPER terms in line_desc" in carrier_line_rule_check(
            LineRule(
                line_rule="BUMPER", message="BUMPER terms in line_desc",
                labor_type_code='OP21', labor_type="mod_lb_hrs",
                labor_operator='>', labor_value=100,
                vehicle_year_condition="OLDER", vehicle_year_count=10,
                mileage_operator=">", mileage_amount=100,
                part_types=["NEW", "USED", "AFTERMARKET"]
            ),
            [EmsLine(line_desc="Frt Bumper Face Bar", line_no=1,
                     lbr_op='OP21', mod_lb_hrs=1500, part_type="PAA")],
            Vehicle(year=2000),
            Ems(v_mileage=200)
        ).message

    def test_none_6(self):
        assert carrier_line_rule_check(
            LineRule(
                line_rule="BUMPER", message="BUMPER terms in line_desc",
                labor_type_code='OP21', labor_type="mod_lb_hrs",
                labor_operator='>', labor_value=100,
                vehicle_year_condition="OLDER", vehicle_year_count=10,
                mileage_operator="<", mileage_amount=100,
                part_types=["NEW", "USED", "AFTERMARKET"]
            ),
            [EmsLine(line_desc="Frt Bumper Face Bar", line_no=1,
                     lbr_op='OP21', mod_lb_hrs=1500, part_type="AD1")],
            Vehicle(year=2000),
            Ems(v_mileage=200)
        ) is None


class TestLineRuleWithNoRule(unittest.TestCase):
    """
    Ems Line attrs: line_desc, mod_lb_hrs
    """
    def test_carrier_line_rules(self):
        assert carrier_line_rule_check(
            LineRule(),
            EmsLine(),
            Vehicle(),
            Ems()
        ) is None


class TestEmsLineDescription(unittest.TestCase):
    """
    Ems Line attrs: line_desc, mod_lb_hrs
    """
    def test_carrier_line_rules(self):
        assert valid_ems_line_description(
            LINE_TERMS[LineRule(line_rule="BUMPER").line_rule],
            EmsLine(line_desc="Frt Bumper Face Bar")
        ) is False
        assert valid_ems_line_description(
            LINE_TERMS[LineRule(line_rule="BUMPER").line_rule],
            EmsLine(line_desc="Frt Bumper")
        ) is True


class TestEmsLineLaborTypeCode(unittest.TestCase):
    """
    Ems Line attrs: line_desc, mod_lb_hrs
    """
    def test_carrier_line_rules(self):
        assert valid_labor_type_code(
            LineRule(), EmsLine(lbr_op="OP10"),
        ) is True
        assert valid_labor_type_code(
            LineRule(labor_type_code='OP23'), EmsLine(),
        ) is True
        assert valid_labor_type_code(
            LineRule(labor_type_code='OP23'), EmsLine(lbr_op="OP10"),
        ) is True
        assert valid_labor_type_code(
            LineRule(labor_type_code='OP23'), EmsLine(lbr_op="OP23"),
        ) is False


class TestEmsLineLaborValue(unittest.TestCase):
    """
    Ems Line attrs: line_desc, mod_lb_hrs
    """
    def test_carrier_line_rules(self):
        assert valid_labor_criteria(
            LineRule(
                labor_type="mod_lb_hrs", labor_operator=None, labor_value=100
            ), EmsLine(mod_lb_hrs=0)
        ) is True
        assert valid_labor_criteria(
            LineRule(
                labor_type="mod_lb_hrs", labor_operator="<", labor_value=100
            ), EmsLine(mod_lb_hrs=None)
        ) is True
        assert valid_labor_criteria(
            LineRule(
                labor_type="mod_lb_hrs", labor_operator=">", labor_value=100
            ), EmsLine(mod_lb_hrs=150)
        ) is False
        assert valid_labor_criteria(
            LineRule(
                labor_type="mod_lb_hrs", labor_operator="<", labor_value=100
            ), EmsLine(mod_lb_hrs=150)
        ) is True
        assert valid_labor_criteria(
            LineRule(
                labor_type="act_price", labor_operator="<", labor_value=100
            ), EmsLine(act_price=150)
        ) is True
        assert valid_labor_criteria(
            LineRule(
                labor_type="act_price", labor_operator=">", labor_value=100
            ), EmsLine(act_price=150)
        ) is False


class TestEmsLineVehicleYear(unittest.TestCase):
    """
    Ems Line attrs: line_desc, mod_lb_hrs
    """
    def test_carrier_line_rules(self):
        assert valid_vehicle_criteria(
            LineRule(
                vehicle_year_condition="OLDER", vehicle_year_count=10
            ), Vehicle(year=None)
        ) is True
        assert valid_vehicle_criteria(
            LineRule(
                vehicle_year_condition=None, vehicle_year_count=10
            ), Vehicle(year=2020)
        ) is True
        assert valid_vehicle_criteria(
            LineRule(
                vehicle_year_condition="OLDER", vehicle_year_count=5
            ), Vehicle(year=2018)
        ) is True
        assert valid_vehicle_criteria(
            LineRule(
                vehicle_year_condition="OLDER", vehicle_year_count=10
            ), Vehicle(year=2008)
        ) is False
        assert valid_vehicle_criteria(
            LineRule(
                vehicle_year_condition="OLDER", vehicle_year_count=5
            ), Vehicle(year=2019)
        ) is True
        assert valid_vehicle_criteria(
            LineRule(
                vehicle_year_condition="NEWER", vehicle_year_count=5
            ), Vehicle(year=2019)
        ) is False
        assert valid_vehicle_criteria(
            LineRule(
                vehicle_year_condition="NEWER", vehicle_year_count=5
            ), Vehicle(year=2014)
        ) is True


class TestEmsMileageValue(unittest.TestCase):
    """
    Ems Line attrs: line_desc, mod_lb_hrs
    """
    def test_carrier_line_rules(self):
        assert valid_mileage_criteria(LineRule(), Ems(v_mileage=100)) is True
        assert valid_mileage_criteria(LineRule(
            mileage_operator=">", mileage_amount=200
        ), Ems(v_mileage=100)) is True
        assert valid_mileage_criteria(LineRule(
            mileage_operator=">", mileage_amount=100
        ), Ems(v_mileage=None)) is True
        assert valid_mileage_criteria(LineRule(
            mileage_operator=">", mileage_amount=150
        ), Ems(v_mileage=100)) is True
        assert valid_mileage_criteria(LineRule(
            mileage_operator="<", mileage_amount=150
        ), Ems(v_mileage=100)) is False


class TestEmsPartTypes(unittest.TestCase):
    """
    Ems Line attrs: line_desc, mod_lb_hrs
    """
    def test_carrier_line_rules(self):
        assert valid_part_type_criteria(
            LineRule(part_types=['NEW']), EmsLine(part_type=None)
        ) is True
        assert valid_part_type_criteria(
            LineRule(part_types=["USED"]), EmsLine(part_type="PAN")
        ) is True
        assert valid_part_type_criteria(
            LineRule(part_types=["NEW"]), EmsLine(part_type="PAN")
        ) is False
        assert valid_part_type_criteria(
            LineRule(part_types=["NEW"]), EmsLine(part_type="PAA")
        ) is True
        assert valid_part_type_criteria(
            LineRule(part_types=["NEW", "USED"]), EmsLine(part_type="PAL")
        ) is False
        assert valid_part_type_criteria(
            LineRule(part_types=["NEW", "USED", "AFTERMARKET"]),
            EmsLine(part_type="PAA")
        ) is False
        assert valid_part_type_criteria(
            LineRule(part_types=["NEW", "USED", "AFTERMARKET"]),
            EmsLine(part_type="AD1")
        ) is True


class EmsLine(object):
    def __init__(self, line_desc=None, mod_lb_hrs=None,
                 line_no=None, lbr_op=None, act_price=None, part_type=None):
        self.line_no = line_no
        self.line_desc = line_desc
        self.mod_lb_hrs = mod_lb_hrs
        self.lbr_op = lbr_op
        self.act_price = act_price
        self.part_type = part_type


class LineRule(object):
    def __init__(self, message="Test Labor info (Bumper), labor hours > 100",
                 severity="WARNING", line_rule=None, field="line_desc",
                 labor_type=None, labor_operator=None,
                 labor_value=None, labor_type_code=None,
                 vehicle_year_condition=None, vehicle_year_count=None,
                 mileage_operator=None, mileage_amount=None, part_types=None):
        self.message = message
        self.severity = severity
        self.line_rule = line_rule
        self.field = field
        self.labor_type = labor_type
        self.labor_operator = labor_operator
        self.labor_value = labor_value
        self.labor_type_code = labor_type_code
        self.vehicle_year_condition = vehicle_year_condition
        self.vehicle_year_count = vehicle_year_count
        self.mileage_operator = mileage_operator
        self.mileage_amount = mileage_amount
        self.part_types = part_types


class Vehicle(object):
    def __init__(self, year=None):
        self.year = year


class Ems(object):
    def __init__(self, v_mileage=None):
        self.v_mileage = v_mileage
