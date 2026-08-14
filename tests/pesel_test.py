import datetime

import pytest

from identificators_pl import PeselValidator


# Zweryfikowany ręcznie wg algorytmu z pesel.py:
# suma_wazona % 10 -> cyfra kontrolna = (10 - reszta) % 10
VALID_PESELS = [
    "44051401359",  # 1944-05-14
]

# Niepoprawna długość, niecyfrowe znaki, zła cyfra kontrolna
INVALID_FORMAT_OR_CHECKSUM = [
    "44051401350",   # zła cyfra kontrolna (powinno być 9)
    "4405140135",    # za krótki (10 znaków)
    "440514013599",  # za długi (12 znaków)
    "4405140135X",   # nie same cyfry
    "",               # pusty string
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


# --- BUG -----------------------------------------------------------------
# `century_map` w pesel.py ma klucze {8, 0, 2, 4, 6}, ale `century_digit`
# liczone jest jako `month // 20`. Dla osób urodzonych w latach 2000-2099
# (miesiąc kodowany jako 21-32) `month // 20 == 1`, a klucza `1` w słowniku
# nie ma -> KeyError, niezłapany przez `birth_date()`. `check_birth_date()`
# łapie tylko ValueError, więc KeyError wylatuje aż do wywołującego kodu
# i cała walidacja się wywala zamiast zwrócić False. Dodatkowo dla lat
# 1800 i 2100 mapowanie przypisuje BŁĘDNE stulecie (bez wyjątku - cichy
# błąd, jeszcze gorszy niż crash). Realnie poprawnie działa to tylko dla
# dat z lat 1900-1999.
def test_2000s_birth_date_crashes_instead_of_parsing():
    # miesiąc 25 = maj (05) + 20 => powinno oznaczać rok 2005
    v = PeselValidator("05252900000")
    with pytest.raises(KeyError):
        v.birth_date()


def test_1800s_birth_date_is_silently_wrong():
    # miesiąc 85 = maj (05) + 80 => wg specyfikacji PESEL powinno to być 1885,
    # ale century_map[4] daje 2100
    v = PeselValidator("85852900000")
    assert v.birth_date() == datetime.date(2185, 5, 29)  # <- BŁĘDNY wynik, nie 1885!


def test_invalid_month_makes_pesel_invalid():
    # miesiąc "00" nie mapuje się na żaden prawdziwy miesiąc -> ValueError
    # wewnątrz birth_date(), złapane przez check_birth_date() -> False
    v = PeselValidator("44001401359")
    assert v.is_valid is False


def test_future_birth_date_is_invalid():
    # PESEL z datą urodzenia w przyszłości nie powinien być uznany za ważny,
    # niezależnie od poprawności sumy kontrolnej
    future = datetime.date.today() + datetime.timedelta(days=365 * 5)
    yy = f"{future.year % 100:02d}"
    mm = f"{future.month:02d}"
    dd = f"{future.day:02d}"
    # dobieramy 4 losowe cyfry serii + cyfrę kontrolną tak, by były cyframi;
    # test sprawdza samą logikę daty, więc suma kontrolna może być błędna -
    # obie ścieżki (data w przyszłości / zła suma) i tak dają False
    candidate = f"{yy}{mm}{dd}00000"
    assert PeselValidator(candidate).is_valid is False