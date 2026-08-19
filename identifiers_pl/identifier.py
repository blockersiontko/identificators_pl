from abc import ABC, abstractmethod


class Identifier(ABC):

    def __init__(self, number: str):
        self.number = number

    @abstractmethod
    def _checksum_valid(self) -> bool: ...

    @abstractmethod
    def _expected_length(self) -> tuple[int, ...]: ...

    def _normalize(self) -> str:
        """Hook for subclasses that need to strip formatting (spaces, case) before
        validating length. Default: no normalization."""
        return self.number

    @property
    def is_valid(self) -> bool:
        return (
            len(self._normalize()) in self._expected_length() and self._checksum_valid()
        )
