import datetime
from polish_identificator import PolishIdentificator


class PeselValidator(PolishIdentificator):

    WEIGHTS = (1, 3, 7, 9, 1, 3, 7, 9, 1, 3)

    def birth_date(self) -> datetime.date:
        year = int(self.number[0:2])
        month = int(self.number[2:4])
        day = int(self.number[4:6])

        century_map = {8: 1800, 0: 1900, 2: 2000, 4: 2100, 6: 2200}

        century_digit = month // 20
        century = century_map[century_digit]
        real_month = month % 20

        full_year = century + year
        return datetime.date(full_year, real_month, day)

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
        return 11
