import unittest

from compliance_checks.ems import (audatex_version, inspection_date,
                                   locked_ems, total_loss, vehicle_mileage,
                                   wrong_header)
from tests.data import Carrier, Ems


class TestEmsHeader(unittest.TestCase):
    def test_wrong_header(self):
        assert wrong_header(Ems()) is True
        assert wrong_header(Ems(ins_co_name=None)) is True
        alert = wrong_header(Ems(ins_co_name='PDA'))
        assert alert.alert == 'WRONG_HEADER'
        assert "ACD MUST BE ON THE HEADER" in alert.message


class TestLockedEms(unittest.TestCase):
    def test_locked_ems(self):
        assert locked_ems(Ems(), Carrier().locked_ems) is True
        assert locked_ems(Ems(status='true'), Carrier().locked_ems) is True

        alert = locked_ems(
            Ems(status='false'),
            Carrier(locked_ems=True).locked_ems
        )
        assert alert.alert == 'ESTIMATE_NOT_LOCKED'
        assert "ESTIMATE NOT LOCKED:" in alert.message


class TestAudatexVersion(unittest.TestCase):
    def test_audatex_version(self):
        assert audatex_version(Ems()) is True
        alert = audatex_version(Ems(ems_ver='2.0'))
        assert alert.alert == 'AUDATEX_VERSION'
        alert = audatex_version(Ems(ems_ver=None))
        assert "AUDATEX EMS VERSION 2.6 OR HIGHER" in alert.message


class TestInspectionDate(unittest.TestCase):
    def test_inspection_date(self):
        assert inspection_date(Ems()) is True
        alert = inspection_date(Ems(insp_date=''))
        assert alert.alert == 'INSPECTION_DATE_MISSING'
        alert = inspection_date(Ems(insp_date=None))
        assert "INSPECTION DATE MUST BE ON YOUR ESTIMATE" in alert.message


class TestTotalLoss(unittest.TestCase):
    def test_inspection_date(self):
        assert total_loss(Ems()) is True
        alert = total_loss(Ems(g_ttl_amt=0))
        assert alert.alert == 'CONFIRM_ESTIMATE_TOTAL'
        alert = total_loss(Ems(g_ttl_amt=None))
        assert "CONFIRM THE TOTAL ESTIMATE AMOUNT" in alert.message


class TestVehicleMileage(unittest.TestCase):
    def test_vehicle_mileage(self):
        assert vehicle_mileage(Ems()) is True
        alert = vehicle_mileage(Ems(v_mileage=0))
        assert alert.alert == 'MILEAGE_MISSING'
        alert = vehicle_mileage(Ems(v_mileage=None))
        assert "MILEAGE MISSING: MILEAGE IS NOT ON" in alert.message
