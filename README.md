# IDENTIFIERS PL

A small tool to validate Polish identifiers: **NIP**, **PESEL**, **REGON** and international **IBAN** (with recognition of whether a country belongs to **SEPA**). Every validator checks number length and its checksum, returning True/False via the `is_valid` property.

# Features

- Abstract base class **Identifier** with `_checksum_valid()` and `_expected_length()` methods;
- Numerical weight-based checksum algorithms according to Polish and international norms;
- **PESEL** century decoding;
- **PESEL** birth-date check, to make sure the **PESEL** number is not from the future;
- **REGON** supporting two length variations (9 and 14 digits);
- **IBAN** validation using ISO 7064 mod-97-10;
- `COUNTRY_LENGTHS` dictionary with expected lengths of **IBAN** numbers per country;
- **SEPA** membership check for a given IBAN country code;
- Dynamic version, read from `VERSION.md`.

# Requirements

- Python 3.11+

# Installation

```bash
pip install identifiers-pl
```

# Usage

```python
from identifiers_pl import NIPValidator, PeselValidator, REGONValidator, IBANValidator

NIPValidator("1234563218").is_valid
PeselValidator("44051401359").is_valid
REGONValidator("123456785").is_valid

iban = IBANValidator("PL61109010140000071219812874")
iban.is_valid
iban.check_sepa
```

# Development

`requirements.txt` contains **development-only** dependencies (`black`, `pytest`, `pytest-cov`) - the package itself has no runtime dependencies.

# License

**MIT License**

# Author

Made by **blocky**