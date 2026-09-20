from toolkit.constants import (
    ABSOLUTE_ZERO_CELSIUS,
    ABSOLUTE_ZERO_FAHRENHEIT,
    ABSOLUTE_ZERO_KELVIN,
    LENGTH_TO_METERS,
    MASS_TO_GRAMS,
    UNIT_GROUPS,
)
from toolkit.errors import (
    AbsoluteZeroError,
    IncompatibleUnitsError,
    InvalidNumberError,
    UnknownUnitError,
)


def convert(value: float | int, from_unit: str, to_unit: str) -> float:
    # 1 Базовые проверки
    if not isinstance(value, int | float):
        raise InvalidNumberError(f"Передано не число: {value}")

    from_u = from_unit.lower()
    to_u = to_unit.lower()

    # 2. Ищем, к каким группам относятся юниты
    from_group = None
    to_group = None

    for group, units in UNIT_GROUPS.items():
        if from_u in units:
            from_group = group
        if to_u in units:
            to_group = group

    if from_group is None:
        raise UnknownUnitError(f"Неизвестная единица: {from_unit}")
    if to_group is None:
        raise UnknownUnitError(f"Неизвестная единица: {to_unit}")

    # 3 Проверка совместимости
    if from_group != to_group:
        raise IncompatibleUnitsError(f"Нельзя конвертировать {from_group} в {to_group}")

    # Если единицы совпадают, просто возвращаем число
    if from_u == to_u:
        return float(value)

    # 4. Обработка температуры (у нее свои формулы)
    if from_group == "temperature":
        # Сначала проверим абсолютный ноль
        if from_u == "c" and value < ABSOLUTE_ZERO_CELSIUS:
            raise AbsoluteZeroError("Температура ниже абсолютного нуля")
        if from_u == "k" and value < ABSOLUTE_ZERO_KELVIN:
            raise AbsoluteZeroError("Температура ниже абсолютного нуля")
        if from_u == "f" and value < ABSOLUTE_ZERO_FAHRENHEIT:
            raise AbsoluteZeroError("Температура ниже абсолютного нуля")

        # Переводим сначала в Цельсии
        if from_u == "c":
            celsius = value
        elif from_u == "f":
            celsius = (value - 32) * 5 / 9
        else:  # kelvin
            celsius = value - 273.15

        # Из Цельсия в нужную шкалу
        if to_u == "c":
            return float(celsius)
        if to_u == "f":
            return float(celsius * 9 / 5 + 32)
        return float(celsius + 273.15)  # to kelvin

    # 5. Обработка длины (через метры)
    if from_group == "length":
        # Сначала в метры, потом в целевую единицу
        meters = value * LENGTH_TO_METERS[from_u]
        return float(meters / LENGTH_TO_METERS[to_u])

    # 6. Обработка массы (через граммы)
    grams = value * MASS_TO_GRAMS[from_u]
    return float(grams / MASS_TO_GRAMS[to_u])
