import pytest

from identifiers_pl import IBANValidator

VALID_IBANS = [
    "PL61109010140000071219812874",
]


INVALID_CHECKSUM_IBANS = [
    "PL61109010140000071219812875",  # ostatnia cyfra zmieniona -> zła suma kontrolna
]


INVALID_LENGTH_IBANS = [
    "PL6110901014000007121981287",  # o jeden znak za krótki
    "PL611090101400000712198128744",  # o jeden znak za długo
]


@pytest.mark.parametrize("iban", VALID_IBANS)
def test_valid_iban(iban):
    assert IBANValidator(iban).is_valid is True


@pytest.mark.parametrize("iban", INVALID_CHECKSUM_IBANS)
def test_invalid_checksum_iban(iban):
    assert IBANValidator(iban).is_valid is False


@pytest.mark.parametrize("iban", INVALID_LENGTH_IBANS)
def test_invalid_length_iban(iban):
    assert IBANValidator(iban).is_valid is False


def test_country_code_is_uppercased():
    v = IBANValidator("pl61109010140000071219812874")
    assert v.country_code == "PL"


@pytest.mark.parametrize(
    "country, expected",
    [
        ("PL", True),  # Polska jest w SEPA
        ("RU", False),  # Rosja ma zdefiniowaną długość, ale nie jest w SEPA
    ],
)
def test_check_sepa(country, expected):
    from identifiers_pl.IBAN.iban_length import COUNTRY_LENGTHS

    length = COUNTRY_LENGTHS[country]
    fake_number = country + "00" + "0" * (length - 4)
    assert IBANValidator(fake_number).check_sepa is expected


def test_invalid_characters_fail_checksum():
    assert IBANValidator("PL6110901014000007121981287!").is_valid is False


def test_unsupported_country_raises_instead_of_returning_false():
    with pytest.raises(ValueError):
        IBANValidator("XX000000000000").is_valid


def test_formatted_iban_with_spaces_is_accepted():
    formatted = "PL 61 1090 1014 0000 0712 1981 2874"
    assert IBANValidator(formatted).is_valid is True
