from toolkit.config_loader import CONFIG_PATH, load_units_config
from toolkit.constants import LENGTH_TO_METERS, UNIT_GROUPS


def test_config_file_exists() -> None:
    """Файл конфигурации units.json существует."""
    assert CONFIG_PATH.exists()


def test_load_units_config_keys() -> None:
    """Конфиг содержит все необходимые таблицы."""
    data = load_units_config()
    assert "length_to_meters" in data
    assert "mass_to_grams" in data
    assert "unit_groups" in data


def test_constants_loaded_from_config() -> None:
    """Константы совпадают с данными из конфигурационного файла."""
    data = load_units_config()
    assert data["length_to_meters"] == LENGTH_TO_METERS
    assert UNIT_GROUPS["length"] == set(data["unit_groups"]["length"])


def test_config_has_all_length_units() -> None:
    """В конфиге есть все единицы длины из задания."""
    data = load_units_config()
    units = set(data["length_to_meters"])
    assert {"mm", "cm", "m", "km"} <= units
