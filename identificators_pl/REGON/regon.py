from ..identificator import Identificator


class REGONValidator(Identificator):

    WEIGHTS_9 = (8, 9, 2, 3, 4, 5, 6, 7)
    WEIGHTS_14 = (2, 4, 8, 5, 0, 9, 7, 3, 6, 1, 2, 4, 8)

    def _checksum_valid(self):
        if not self.number.isdigit():
            return False
        digits = [int(d) for d in self.number]
        if len(self.number) == 9:
            checksum = sum(w * d for w, d in zip(self.WEIGHTS_9, digits[:-1])) % 11
        elif len(self.number) == 14:
            checksum = sum(w * d for w, d in zip(self.WEIGHTS_14, digits[:-1])) % 11
        else:
            return False

        if checksum == 10:
            return digits[-1] == 0
        
        return checksum == digits[-1]

    def _expected_length(self):
        return (9, 14)