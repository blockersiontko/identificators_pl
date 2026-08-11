from abc import ABC, abstractmethod


class PolishIdentificator(ABC):

    def __init__(self, number: str):
        self.number = number

    @abstractmethod
    def _checksum_valid(self) -> bool: ...

    @abstractmethod
    def _expected_length(self) -> int: ...

    @property
    def is_valid(self) -> bool:
        return len(self.number) == self._expected_length() and self._checksum_valid()
