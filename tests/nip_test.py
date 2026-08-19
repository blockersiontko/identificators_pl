import pytest

from identifiers_pl import NIPValidator

VALID_NIPS = [
    "5260001246",
]


INVALID_NIPS = [
    "5260001240",  # zła cyfra kontrolna
    "526000124",  # za krótki
    "52600012466",  # za długi
    "526000124A",  # nie same cyfry
    "",
]


@pytest.mark.parametrize("nip", VALID_NIPS)
def test_valid_nip(nip):
    assert NIPValidator(nip).is_valid is True


@pytest.mark.parametrize("nip", INVALID_NIPS)
def test_invalid_nip(nip):
    assert NIPValidator(nip).is_valid is False


def test_nip_with_dashes_is_not_normalized():
    assert NIPValidator("526-000-12-46").is_valid is False
