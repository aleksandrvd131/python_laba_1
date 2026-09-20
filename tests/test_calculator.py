import pytest
from toolkit.calculator import calculate
from toolkit.errors import (
    ConsecutiveOperatorsError,
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidCharacterError,
    MismatchedParenthesesError,
)


class TestCalculatorPositive:
    def test_simple_addition(self) -> None:
        assert calculate("2 + 3") == 5.0

    def test_priority(self) -> None:
        assert calculate("2 + 2 * 2") == 6.0

    def test_parentheses(self) -> None:
        assert calculate("(2 + 2) * 2") == 8.0

    def test_unary_minus(self) -> None:
        assert calculate("-5 + 10") == 5.0

    def test_multi_digit_numbers(self) -> None:
        assert calculate("123 + 456") == 579.0

    def test_division(self) -> None:
        assert calculate("10 / 4") == 2.5

    def test_integer_division(self) -> None:
        assert calculate("10 // 3") == 3.0

    def test_modulo(self) -> None:
        assert calculate("10 % 3") == 1.0


class TestCalculatorNegative:
    def test_division_by_zero(self) -> None:
        with pytest.raises(DivisionByZeroError):
            calculate("10 / 0")

    def test_empty_expression(self) -> None:
        with pytest.raises(EmptyExpressionError):
            calculate("")

    def test_invalid_character(self) -> None:
        with pytest.raises(InvalidCharacterError):
            calculate("2 + a")

    def test_consecutive_operators(self) -> None:
        with pytest.raises(ConsecutiveOperatorsError):
            calculate("2 + * 3")

    def test_mismatched_parentheses(self) -> None:
        with pytest.raises(MismatchedParenthesesError):
            calculate("(2 + 3")
