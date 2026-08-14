import datetime
from ..identificator import Identificator


class PeselValidator(Identificator):

    WEIGHTS = (1, 3, 7, 9, 1, 3, 7, 9, 1, 3)

    def birth_date(self) -> datetime.date:
        year = int(self.number[0:2])
        month = int(self.number[2:4])
        day = int(self.number[4:6])

        if 81 <= month <= 92:
            century = 1800
            month -= 80
        elif 1 <= month <= 12:
            century = 1900
        elif 21 <= month <= 32:
            century = 2000
            month -= 20
        elif 41 <= month <= 52:
            century = 2100
            month -= 40
        elif 61 <= month <= 72:
            century = 2200
            month -= 60
        else:
            raise ValueError('Invalid PESEL month')

        full_year = century + year
        return datetime.date(full_year, month, day)

    def check_birth_date(self) -> bool:
        todays_date = datetime.date.today()
        try:
            born = self.birth_date()
        except ValueError:
            return False
        return todays_date >= born

    def _checksum_valid(self) -> bool:
        if not self.number.isdigit():
            return False
        if not self.check_birth_date():
            return False
        digits = [int(d) for d in self.number]
        checksum = sum(w * d for w, d in zip(self.WEIGHTS, digits)) % 10
        control_digit = (10 - checksum) % 10
        return control_digit == digits[10]

    def _expected_length(self) -> int:
        return (11, )