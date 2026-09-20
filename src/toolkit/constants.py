from typing import Final

# Коэффициенты для перевода длины в базовую единицу (метры)
LENGTH_TO_METERS: Final[dict[str, float]] = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
}

# Коэффициенты для перевода массы в базовую единицу (граммы)
MASS_TO_GRAMS: Final[dict[str, float]] = {
    "g": 1.0,
    "kg": 1000.0,
}

# Группировка единиц измерения для проверки совместимости
UNIT_GROUPS: Final[dict[str, set[str]]] = {
    "length": {"mm", "cm", "m", "km"},
    "mass": {"g", "kg"},
    "temperature": {"c", "f", "k"},
}

# Значения абсолютного нуля для разных шкал
ABSOLUTE_ZERO_CELSIUS: Final[float] = -273.15
ABSOLUTE_ZERO_KELVIN: Final[float] = 0.0
ABSOLUTE_ZERO_FAHRENHEIT: Final[float] = -459.67
