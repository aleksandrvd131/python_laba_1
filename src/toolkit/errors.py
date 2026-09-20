"""Кастомные исключения для нашего пакета."""


class ToolkitError(Exception):
    """Базовое исключение для всех ошибок тулкита."""

    pass


class EmptyExpressionError(ToolkitError):
    """Вызывается, когда передано пустое выражение."""

    pass


class InvalidCharacterError(ToolkitError):
    """Вызывается при встрече недопустимого символа."""

    pass


class MissingOperandError(ToolkitError):
    """Вызывается, когда оператору не хватает операнда."""

    pass


class ConsecutiveOperatorsError(ToolkitError):
    """Вызывается, когда два бинарных оператора идут подряд."""

    pass


class DivisionByZeroError(ToolkitError):
    """Вызывается при попытке деления на ноль."""

    pass


class UnknownUnitError(ToolkitError):
    """Вызывается при передаче неизвестной единицы измерения."""

    pass


class IncompatibleUnitsError(ToolkitError):
    """Вызывается при попытке сконвертировать разные группы (например, метры в кг)."""

    pass


class InvalidNumberError(ToolkitError):
    """Вызывается, если вместо числа передана ерунда."""

    pass


class AbsoluteZeroError(ToolkitError):
    """Вызывается, если температура ниже абсолютного нуля."""

    pass


class MismatchedParenthesesError(ToolkitError):
    """Вызывается при несбалансированных скобках."""

    pass
