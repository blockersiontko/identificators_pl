from polish_identificator import PolishIdentificator
from iban_length import COUNTRY_LENGTHS


class IBANValidator(PolishIdentificator):

    @property
    def country_code(self) -> str:
        return self.number[:2].upper()

    def _normalized_number(self) -> str:
        return self.number.upper().replace(" ", "")

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

    def _expected_length(self) -> int:
        try:
            return COUNTRY_LENGTHS[self.country_code]
        except KeyError:
            raise ValueError(f"Unsupported IBAN country: {self.country_code}")

    # can add bban check in future
