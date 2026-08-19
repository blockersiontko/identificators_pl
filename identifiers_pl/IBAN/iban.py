from ..identifier import Identifier
from .iban_length import COUNTRY_LENGTHS
from .sepa import SEPA_COUNTRIES


class IBANValidator(Identifier):

    @property
    def country_code(self) -> str:
        return self._normalized_number()[:2]

    @property
    def check_sepa(self) -> bool:
        return self.country_code in SEPA_COUNTRIES

    def _normalized_number(self) -> str:
        return self.number.upper().replace(" ", "")

    def _normalize(self) -> str:
        return self._normalized_number()

    def _checksum_valid(self) -> bool:

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
        if length is None:
            raise ValueError(f"Unsupported country code {self.country_code}")
        return (length,)

    # can add bban check in future
