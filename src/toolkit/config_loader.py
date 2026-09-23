import json
from pathlib import Path
from typing import Any, Final

# Путь к конфигу: файл лежит рядом с кодом пакета
CONFIG_PATH: Final[Path] = Path(__file__).resolve().parent / "units.json"


def load_units_config() -> dict[str, Any]:
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)
    return data
