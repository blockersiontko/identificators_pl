from polish_identificator import PolishIdentificator


class NIPValidator(PolishIdentificator):

    WEIGHTS = (6, 5, 7, 2, 3, 4, 5, 6, 7)

    def _checksum_valid(self) -> bool:
            if not self.number.isdigit():
                 return False
            digits = [int(d) for d in self.number]
            checksum = sum(w * d for w, d in zip(self.WEIGHTS, digits[:-1])) % 11
            return checksum == digits[-1]

    def _expected_length(self):
        return 10