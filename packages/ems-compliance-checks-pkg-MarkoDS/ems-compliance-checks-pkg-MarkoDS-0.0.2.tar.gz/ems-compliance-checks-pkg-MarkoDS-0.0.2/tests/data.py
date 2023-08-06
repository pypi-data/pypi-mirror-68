class Claim(object):
    def __init__(self, claim_number='Test', deductible=0.00):
        self.claim_number = claim_number
        self.deductible = deductible


class Ems(object):
    def __init__(
            self, clm_no='Test', g_ded_amt=0.00, ins_co_name='ACD', status='1',
            est_system='A', ems_ver='2.6', insp_date='2020-01-01',
            g_ttl_amt=100, v_mileage=100
    ):
        self.clm_no = clm_no
        self.g_ded_amt = g_ded_amt
        self.ins_co_name = ins_co_name
        self.status = status
        self.est_system = est_system
        self.ems_ver = ems_ver
        self.insp_date = insp_date
        self.g_ttl_amt = g_ttl_amt
        self.v_mileage = v_mileage


class Carrier(object):
    def __init__(self, locked_ems=True):
        self.locked_ems = locked_ems


class CarrierLineRule(object):
    def __init__(self, field='line_desc', line_rule='BUMPER', line_terms=None,
                 labor_type_code=None, labor_type='act_price',
                 labor_operator='<', labor_value='4', vehicle_year_count='1',
                 vehicle_year_condition='OLDER', vehicle_operator=None,
                 vehicle_year=2018, mileage_operator='>', mileage_amount=15000,
                 part_types='NEW',
                 message='Reconditioned lamps should be utilized on vehicles',
                 severity='WARNING'
    ):
        self.field = field
        self.line_rule = line_rule
        self.line_terms = line_terms
        self.labor_type_code = labor_type_code
        self.labor_type = labor_type
        self.labor_operator = labor_operator
        self.labor_value = labor_value
        self.vehicle_year_count = vehicle_year_count
        self.vehicle_year_condition = vehicle_year_condition
        self.vehicle_operator = vehicle_operator
        self.vehicle_year = vehicle_year
        self.mileage_operator = mileage_operator
        self.mileage_amount = mileage_amount
        self.part_types = part_types
        self.message = message
        self.severity = severity


class EmsLine(object):
    def __init__(self, line_desc='Frt Bumper Assy', act_price='100',
                 mod_lb_hrs='1', part_type='PAM'
    ):
        self.line_desc = line_desc
        self.act_price = act_price
        self.mod_lb_hrs = mod_lb_hrs
        self.part_type = part_type


class Vehicle(object):
    def __init__(self, year=2020):
        self.year = year
