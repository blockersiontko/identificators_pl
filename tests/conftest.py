"""
Konfiguracja testów.

Testy zakładają, że pakiet `identificators_pl` jest zainstalowany
(np. `pip install -e .` z katalogu głównego repo) albo że katalog
z pakietem jest na PYTHONPATH. Jeśli uruchamiasz testy z katalogu
repo bez instalacji, ten plik dokłada katalog nadrzędny do sys.path.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))