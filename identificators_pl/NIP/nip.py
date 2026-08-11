import datetime
from polish_identificator import PolishIdentificator


class NIPValidator(PolishIdentificator):

    def nip(self):
        pass

    def _checksum_valid(self):
        return super()._checksum_valid()

    def _expected_length(self):
        return super()._expected_length()
