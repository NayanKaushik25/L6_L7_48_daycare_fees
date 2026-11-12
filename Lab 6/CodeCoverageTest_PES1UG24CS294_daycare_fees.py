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


def test_sibling_included_hours():
    # Toddler gets 25 included hours + 5 sibling hours
    assert extra_hours_fee("toddler", 30, True) == 0


def test_infant_regular_extra_hours():
    # Infant: 20 included, 5 extra at rate 14
    assert extra_hours_fee("infant", 25, False) == 70


def test_non_infant_regular_extra_hours():
    # Toddler: 25 included, 5 extra at rate 9
    assert extra_hours_fee("toddler", 30, False) == 45


def test_non_infant_more_than_20_extra_hours():
    # Toddler: 25 included, 25 extra at rate 9 + 5
    assert extra_hours_fee("toddler", 50, False) == 350


def test_infant_more_than_20_extra_hours():
    # Infant: 20 included, 25 extra at rate 14 + 5 + 3
    assert extra_hours_fee("infant", 45, False) == 550


# --------------------------------------------------
# Tests for enrolment_allowed()
# --------------------------------------------------

def test_enrolment_pending_immunisation_allowed():
    assert enrolment_allowed(24, 0, True) is True


def test_enrolment_pending_immunisation_under_12_months():
    assert enrolment_allowed(10, 5, True) is False


def test_enrolment_under_6_months():
    assert enrolment_allowed(5, 2, False) is False


def test_enrolment_no_vacancies():
    assert enrolment_allowed(24, 0, False) is False


def test_enrolment_with_vacancies():
    assert enrolment_allowed(24, 2, False) is True


# --------------------------------------------------
# Tests for pickup_status()
# --------------------------------------------------

def test_pickup_on_time():
    # Non-aftercare, Friday: cutoff = 10 + 10 = 20
    assert pickup_status(20, False, True) == "on_time"


def test_pickup_late():
    # Aftercare, not Friday: cutoff = 20
    assert pickup_status(10, True, False) == "late"


def test_pickup_overdue():
    # Aftercare, Friday: cutoff = 20 + 10 = 30
    assert pickup_status(14, True, True) == "overdue"
