from typing import Final

from toolkit.config_loader import load_units_config

# Загружаем таблицы конвертации из JSON-конфига
_config = load_units_config()

# Коэффициенты для перевода длины в базовую единицу (метры)
LENGTH_TO_METERS: Final[dict[str, float]] = _config["length_to_meters"]

# Коэффициенты для перевода массы в базовую единицу (граммы)
MASS_TO_GRAMS: Final[dict[str, float]] = _config["mass_to_grams"]

# Группировка единиц измерения для проверки совместимости
UNIT_GROUPS: Final[dict[str, set[str]]] = {
    group: set(units) for group, units in _config["unit_groups"].items()
}

# Значения абсолютного нуля для разных шкал
ABSOLUTE_ZERO_CELSIUS: Final[float] = -273.15
ABSOLUTE_ZERO_KELVIN: Final[float] = 0.0
ABSOLUTE_ZERO_FAHRENHEIT: Final[float] = -459.67

# Точность вычислений: количество значащих цифр
DECIMAL_PRECISION: Final[int] = 28
# Количество знаков после запятой в итоговом результате
RESULT_DECIMAL_PLACES: Final[int] = 6
