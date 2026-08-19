from importlib.metadata import version, PackageNotFoundError

from .IBAN import IBANValidator
from .NIP import NIPValidator
from .REGON import REGONValidator
from .PESEL import PeselValidator

__all__ = [
    "IBANValidator",
    "NIPValidator",
    "REGONValidator",
    "PeselValidator",
]

try:
    __version__ = version("identificators-pl")
except PackageNotFoundError:
    __version__ = "unknown"
