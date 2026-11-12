import pytest
from daycare_fees import extra_hours_fee, enrolment_allowed, pickup_status


# --------------------------------------------------
# Tests for extra_hours_fee()
# --------------------------------------------------

def test_unknown_age_group():
    with pytest.raises(ValueError):
        extra_hours_fee("school", 30, False)


def test_negative_hours():
    with pytest.raises(ValueError):
        extra_hours_fee("toddler", -5, False)


def test_included_hours_without_sibling():
    assert extra_hours_fee("toddler", 20, False) == 0


def test_sibling_extra_hours():
    # Sibling gets 5 additional included hours
    assert extra_hours_fee("toddler", 30, True) == 0


def test_infant_with_sibling():
    # Infant does not receive additional sibling hours
    assert extra_hours_fee("infant", 20, True) == 0


def test_infant_regular_extra_hours():
    assert extra_hours_fee("infant", 25, False) == 70


def test_non_infant_regular_extra_hours():
    assert extra_hours_fee("preschool", 35, False) == 45


def test_infant_more_than_20_extra_hours():
    # Exercises extra > 20 and nested infant condition
    assert extra_hours_fee("infant", 45, False) == 550


def test_non_infant_more_than_20_extra_hours():
    # Exercises extra > 20 and nested infant false condition
    assert extra_hours_fee("toddler", 50, False) == 350


# --------------------------------------------------
# Tests for enrolment_allowed()
# --------------------------------------------------

def test_pending_immunisation_age_eligible():
    assert enrolment_allowed(12, 0, True) is True


def test_pending_immunisation_age_ineligible():
    assert enrolment_allowed(10, 5, True) is False


def test_age_below_6_months():
    assert enrolment_allowed(5, 2, False) is False


def test_age_above_6_months_without_vacancies():
    assert enrolment_allowed(24, 0, False) is False


def test_age_above_6_months_with_vacancies():
    assert enrolment_allowed(24, 2, False) is True


# --------------------------------------------------
# Tests for pickup_status()
# --------------------------------------------------

def test_aftercare_friday_on_time():
    # Cutoff = 20 + 10 = 30
    assert pickup_status(30, True, True) == "on_time"


def test_non_aftercare_non_friday_on_time():
    # Cutoff = 10
    assert pickup_status(10, False, False) == "on_time"


def test_aftercare_late():
    # Cutoff = 20; 10 minutes left is late
    assert pickup_status(10, True, False) == "late"


def test_non_aftercare_friday_late():
    # Cutoff = 20; 10 minutes left is late
    assert pickup_status(10, False, True) == "late"


def test_aftercare_friday_overdue():
    # Cutoff = 30; 14 minutes left is overdue
    assert pickup_status(14, True, True) == "overdue"
