import pytest

from identificators_pl import IBANValidator


# Klasyczny przykładowy poprawny polski IBAN (m.in. z Wikipedii),
# spełnia mod-97 == 1 zgodnie z algorytmem ISO 7064.
VALID_IBANS = [
    "PL61109010140000071219812874",
]

INVALID_CHECKSUM_IBANS = [
    "PL61109010140000071219812875",  # ostatnia cyfra zmieniona -> zła suma kontrolna
]

INVALID_LENGTH_IBANS = [
    "PL6110901014000007121981287",   # o jeden znak za krótki
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
        ("PL", True),   # Polska jest w SEPA
        ("RU", False),  # Rosja ma zdefiniowaną długość, ale nie jest w SEPA
    ],
)
def test_check_sepa(country, expected):
    # budujemy numer o poprawnej długości dla danego kraju (treść numeryczna
    # nieistotna dla samej flagi check_sepa)
    from identificators_pl.IBAN.iban_length import COUNTRY_LENGTHS

    length = COUNTRY_LENGTHS[country]
    fake_number = country + "00" + "0" * (length - 4)
    assert IBANValidator(fake_number).check_sepa is expected


def test_invalid_characters_fail_checksum():
    # znak spoza [0-9A-Z] po normalizacji -> _checksum_valid zwraca False
    assert IBANValidator("PL6110901014000007121981287!").is_valid is False


# --- BUG -----------------------------------------------------------------
# `Identificator.is_valid` woła `self._expected_length()`, a
# `IBANValidator._expected_length()` rzuca ValueError dla nieobsługiwanego
# kodu kraju. `is_valid` tego wyjątku nie łapie, więc zamiast zwrócić
# False, cała walidacja się wywala. To może zaskoczyć każdego, kto robi
# `if validator.is_valid:` na niezaufanym wejściu użytkownika.
def test_unsupported_country_raises_instead_of_returning_false():
    with pytest.raises(ValueError):
        IBANValidator("XX000000000000").is_valid


# --- BUG -----------------------------------------------------------------
# `_expected_length()` porównuje długość znormalizowanego numeru wg
# COUNTRY_LENGTHS, ale `Identificator.is_valid` liczy `len(self.number)`
# na SUROWYM, niezmodyfikowanym numerze - spacje nie są usuwane przed tym
# porównaniem (normalizacja dzieje się tylko wewnątrz `_checksum_valid`).
# Efekt: poprawny, ale sformatowany spacjami IBAN (typowy sposób zapisu
# na przelewach/w bankowości) zawsze zostanie odrzucony jako "zła długość".
def test_formatted_iban_with_spaces_is_incorrectly_rejected():
    formatted = "PL 61 1090 1014 0000 0712 1981 2874"
    assert IBANValidator(formatted).is_valid is False  # oczekiwalibyśmy True