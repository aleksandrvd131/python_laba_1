import pytest
from toolkit.calculator import calculate
from toolkit.errors import (
    ConsecutiveOperatorsError,
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterError,
    MismatchedParenthesesError,
)


def test_simple_addition() -> None:
    # Простое сложение
    assert calculate("2 + 3") == 5.0


def test_priority() -> None:
    # Приоритет операций: умножение раньше сложения
    assert calculate("2 + 2 * 2") == 6.0


def test_parentheses() -> None:
    # Скобки меняют приоритет
    assert calculate("(2 + 2) * 2") == 8.0


def test_unary_minus() -> None:
    # Унарный минус перед числом
    assert calculate("-5 + 10") == 5.0


def test_multi_digit_numbers() -> None:
    # Многозначные числа
    assert calculate("123 + 456") == 579.0


def test_division() -> None:
    # Обычное деление
    assert calculate("10 / 4") == 2.5


def test_integer_division() -> None:
    # Целочисленное деление
    assert calculate("10 // 3") == 3.0


def test_modulo() -> None:
    # Остаток от деления
    assert calculate("10 % 3") == 1.0


def test_decimal_exactness() -> None:
    # 0.1 + 0.2 должно быть ровно 0.3 благодаря Decimal
    assert calculate("0.1 + 0.2") == 0.3


def test_rounding_half_up() -> None:
    # Политика ROUND_HALF_UP: половина округляется вверх
    assert calculate("2.0000005") == 2.000001


def test_floor_division_negative() -> None:
    # Целочисленное деление с минусом как в Python: -7 // 2 = -4
    assert calculate("-7 // 2") == -4.0


def test_modulo_negative() -> None:
    # Остаток с минусом как в Python: -10 % 3 = 2
    assert calculate("-10 % 3") == 2.0


def test_division_by_zero() -> None:
    # Деление на нол
    with pytest.raises(DivisionByZeroError):
        calculate("10 / 0")


def test_empty_expression() -> None:
    # Пустое выражение#
    with pytest.raises(EmptyExpressionError):
        calculate("")


def test_invalid_character() -> None:
    # Недопустимый символ
    with pytest.raises(InvalidCharacterError):
        calculate("2 + a")


def test_consecutive_operators() -> None:
    # Два оператора подряд
    with pytest.raises(ConsecutiveOperatorsError):
        calculate("2 + * 3")


def test_mismatched_parentheses() -> None:
    # Нeзакрытая скобка
    with pytest.raises(MismatchedParenthesesError):
        calculate("(2 + 3")
