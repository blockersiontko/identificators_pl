from ..identificator import Identificator
from .iban_length import COUNTRY_LENGTHS
from .sepa import SEPA_COUNTRIES


class IBANValidator(Identificator):

    @property
    def country_code(self) -> str:
        return self._normalized_number()[:2]
    
    @property
    def check_sepa(self) -> bool:
        return self.country_code in SEPA_COUNTRIES

    def _normalized_number(self) -> str:
        return self.number.upper().replace(" ", "")

    def _checksum_valid(self) -> bool:

        expected_length = self._expected_length()
        if expected_length == 0:
            return False

        number = self._normalized_number()
        rearranged = number[4:] + number[:4]

        numeric_string = ""
        for char in rearranged:
            if char.isdigit():
                numeric_string += char
            elif "A" <= char <= "Z":
                numeric_string += str(ord(char) - ord("A") + 10)
            else:
                return False

        return int(numeric_string) % 97 == 1

    def _expected_length(self) -> tuple[int, ...]:
        length = COUNTRY_LENGTHS.get(self.country_code)
        return (length,) if length else ()

    # can add bban check in future