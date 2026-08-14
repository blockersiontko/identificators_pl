import pytest

from identificators_pl import NIPValidator


# 5260001246 zweryfikowany ręcznie wg wag (6,5,7,2,3,4,5,6,7):
# 5*6+2*5+6*7+0*2+0*3+0*4+1*5+2*6+4*7 = 127; 127 % 11 = 6 -> cyfra kontrolna 6 ✔
VALID_NIPS = [
    "5260001246",
]

INVALID_NIPS = [
    "5260001240",   # zła cyfra kontrolna
    "526000124",    # za krótki
    "52600012466",  # za długi
    "526000124A",   # nie same cyfry
    "",
]


@pytest.mark.parametrize("nip", VALID_NIPS)
def test_valid_nip(nip):
    assert NIPValidator(nip).is_valid is True


@pytest.mark.parametrize("nip", INVALID_NIPS)
def test_invalid_nip(nip):
    assert NIPValidator(nip).is_valid is False


def test_nip_with_dashes_is_not_normalized():
    # NIPValidator nie usuwa myślników/spacji - to jest zamierzone
    # zachowanie tej implementacji (w przeciwieństwie do IBANValidator,
    # który normalizuje numer). Ten test dokumentuje obecne zachowanie.
    assert NIPValidator("526-000-12-46").is_valid is False