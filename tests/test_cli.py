import subprocess
import sys


class TestCLI:
    # Тесты командной строки

    def test_calc_success(self) -> None:
        # успешное вычисление через CLI
        result = subprocess.run(
            [sys.executable, "-m", "toolkit", "calc", "2 + 2"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "4.0"

    def test_calc_error(self) -> None:
        # ошибка деления на ноль через CLI
        result = subprocess.run(
            [sys.executable, "-m", "toolkit", "calc", "10 / 0"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 2
        assert "Деление на ноль" in result.stderr

    def test_convert_success(self) -> None:
        # успешная конвертация через CLI
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "toolkit",
                "convert",
                "100",
                "--from",
                "cm",
                "--to",
                "m",
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "1.0"
