import pytest

from identifiers_pl import REGONValidator

# Poprawne (zweryfikowane ręcznie) numery REGON wg algorytmów w regon.py
VALID_REGON_9 = [
    "000331501"
]  # rzeczywisty REGON GUS, suma kontrolna zgodna z wagami 8-cyfrowymi
VALID_REGON_14 = [
    "00033150100017"
]  # 9-cyfrowy prefiks + jednostka lokalna, suma kontrolna zgodna z WEIGHTS_14

INVALID_REGON = [
    "000331500",  # zła cyfra kontrolna (9-cyfrowy)
    "00033150100010",  # zła cyfra kontrolna (14-cyfrowy)
    "12345",  # zła długość
    "12345678A",  # nie same cyfry
    "",
]


@pytest.mark.parametrize("regon", VALID_REGON_9 + VALID_REGON_14)
def test_valid_regon_is_valid(regon):
    assert REGONValidator(regon).is_valid is True


@pytest.mark.parametrize("regon", INVALID_REGON)
def test_invalid_regon_is_invalid(regon):
    assert REGONValidator(regon).is_valid is False


# Ten test NIE zależy od buga w is_valid - testuje bezpośrednio
# metodę wewnętrzną _checksum_valid(), która liczy poprawnie.
@pytest.mark.parametrize("regon", VALID_REGON_9 + VALID_REGON_14)
def test_checksum_valid_directly(regon):
    assert REGONValidator(regon)._checksum_valid() is True


@pytest.mark.parametrize("regon", INVALID_REGON)
def test_checksum_invalid_directly(regon):
    assert REGONValidator(regon)._checksum_valid() is False
