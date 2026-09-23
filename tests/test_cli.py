import subprocess
import sys
from pathlib import Path


def _run_toolkit(
    args: list[str],
    cwd: Path,
) -> subprocess.CompletedProcess[str]:
    # Запускает toolkit в изолированной временной папке
    return subprocess.run(
        [sys.executable, "-m", "toolkit", *args],
        capture_output=True,
        text=True,
        cwd=cwd,
    )


def test_calc_success(tmp_path: Path) -> None:
    # Успешное вычисление через CLI
    result = _run_toolkit(["calc", "2 + 2"], tmp_path)
    assert result.returncode == 0
    assert result.stdout.strip() == "4.0"


def test_calc_error(tmp_path: Path) -> None:
    # Ошибка деления на ноль через CLI
    result = _run_toolkit(["calc", "10 / 0"], tmp_path)
    assert result.returncode == 2
    assert "Деление на ноль" in result.stderr


def test_convert_success(tmp_path: Path) -> None:
    # Успешная конвертация через CLI
    result = _run_toolkit(
        ["convert", "100", "--from", "cm", "--to", "m"],
        tmp_path,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "1.0"


def test_convert_negative_value(tmp_path: Path) -> None:
    # Конвертация отрицательной температуры через CLI
    result = _run_toolkit(
        ["convert", "-40", "--from", "c", "--to", "f"],
        tmp_path,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "-40.0"


def test_calc_unary_minus(tmp_path: Path) -> None:
    # Выражение с унарным минусом в начале через CLI
    result = _run_toolkit(["calc", "-5 + 10"], tmp_path)
    assert result.returncode == 0
    assert result.stdout.strip() == "5.0"


def test_help_exit_code(tmp_path: Path) -> None:
    # Команда --help завершается с кодом 0
    result = _run_toolkit(["--help"], tmp_path)
    assert result.returncode == 0
