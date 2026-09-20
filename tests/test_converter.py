import pytest
from toolkit.converter import convert
from toolkit.errors import (
    AbsoluteZeroError,
    IncompatibleUnitsError,
    UnknownUnitError,
)


class TestConverterPositive:
    # + тесты конвертера

    def test_length_cm_to_m(self) -> None:
        assert convert(100, "cm", "m") == 1.0

    def test_mass_kg_to_g(self) -> None:
        assert convert(2, "kg", "g") == 2000.0

    def test_temperature_f_to_c(self) -> None:
        assert convert(32, "f", "c") == 0.0

    def test_case_insensitive(self) -> None:
        assert convert(100, "CM", "M") == 1.0


class TestConverterNegative:
    def test_unknown_unit(self) -> None:
        with pytest.raises(UnknownUnitError):
            convert(10, "m", "xyz")

    def test_incompatible_units(self) -> None:
        with pytest.raises(IncompatibleUnitsError):
            convert(10, "m", "kg")

    def test_below_absolute_zero(self) -> None:
        with pytest.raises(AbsoluteZeroError):
            convert(-300, "c", "k")
