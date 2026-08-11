import datetime
from polish_identificator import PolishIdentificator

class IBANValidator(PolishIdentificator):

    def iban(self):
        pass

    def _checksum_valid(self):
        number = self.number.upper().replace(" ", "")
        rearranged = number[4:] + number[:4]

        numeric_string = ""
        for char in rearranged:
            if char.isdigit():
                numeric_string += char
            elif char.isalpha():
                numeric_string += str(ord(char) - ord('A') + 10)
            else:
                return False

        return int(numeric_string) % 97 == 1

    def _expected_length(self):
        return 28