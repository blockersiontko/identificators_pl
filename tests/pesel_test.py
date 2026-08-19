import datetime

import pytest

from identifiers_pl import PeselValidator

VALID_PESELS = [
    "44051401359",  # 1944-05-14
]


INVALID_FORMAT_OR_CHECKSUM = [
    "44051401350",  # zła cyfra kontrolna (powinno być 9)
    "4405140135",  # za krótki (10 znaków)
    "440514013599",  # za długi (12 znaków)
    "4405140135X",  # nie same cyfry
    "",  # pusty string
]


@pytest.mark.parametrize("pesel", VALID_PESELS)
def test_valid_pesel_is_valid(pesel):
    assert PeselValidator(pesel).is_valid is True


@pytest.mark.parametrize("pesel", INVALID_FORMAT_OR_CHECKSUM)
def test_invalid_format_or_checksum_pesel(pesel):
    assert PeselValidator(pesel).is_valid is False


def test_birth_date_parsed_correctly():
    v = PeselValidator("44051401359")
    assert v.birth_date() == datetime.date(1944, 5, 14)


def test_2000s_birth_date_parses_correctly():
    v = PeselValidator("05252900000")
    assert v.birth_date() == datetime.date(2005, 5, 29)


def test_1800s_birth_date_parses_correctly():
    v = PeselValidator("85852900000")
    assert v.birth_date() == datetime.date(1885, 5, 29)


def test_invalid_month_makes_pesel_invalid():
    v = PeselValidator("44001401359")
    assert v.is_valid is False


def test_future_birth_date_is_invalid():
    future = datetime.date.today() + datetime.timedelta(days=365 * 5)
    yy = f"{future.year % 100:02d}"
    mm = f"{future.month:02d}"
    dd = f"{future.day:02d}"
    candidate = f"{yy}{mm}{dd}00000"
    assert PeselValidator(candidate).is_valid is False
