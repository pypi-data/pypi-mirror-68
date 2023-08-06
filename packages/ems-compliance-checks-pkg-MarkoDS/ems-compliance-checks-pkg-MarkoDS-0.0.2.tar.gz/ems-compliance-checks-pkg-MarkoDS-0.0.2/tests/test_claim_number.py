import unittest

from compliance_checks.claim_number import (ems_with_claim_number,
                                            match_claim_number,
                                            match_deductible)
from tests.data import Claim, Ems


class TestMatchingClaimNumber(unittest.TestCase):
    @staticmethod
    def test_match_claim_number():
        assert match_claim_number(
            Claim(), Ems()
        ) is True

        alert = match_claim_number(
            Claim(claim_number='Testing'), Ems(clm_no=None)
        )

        assert alert.alert == 'WRONG_CLAIM_NUMBER'
        assert "CLAIM NUMBER DOESN'T MATCH" in alert.message


class TestEmsWithClaimNumber(unittest.TestCase):
    @staticmethod
    def test_ems_with_claim_number():
        assert ems_with_claim_number(
            Ems()
        ) is True

        alert = ems_with_claim_number(
            Ems(clm_no=None)
        )

        assert alert.alert == 'CLAIM_NUMBER_MISSING'
        assert "CLAIM NUMBER MUST BE ON YOUR ESTIMATE" in alert.message


class TestMatchDeductible(unittest.TestCase):
    @staticmethod
    def test_match_deductible():
        assert match_deductible(
            Claim(),
            Ems()
        ) is True

        alert = match_deductible(
            Claim(deductible=1.00),
            Ems()
        )

        assert alert.alert == 'WRONG_DEDUCTIBLE'
        assert "DEDUCTIBLE DOESN'T MATCH" in alert.message
