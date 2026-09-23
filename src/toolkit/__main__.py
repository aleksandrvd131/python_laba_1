import sys

import typer

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import InvalidNumberError, ToolkitError
from toolkit.history import save_to_history

# Разрешаем аргументы, начинающиеся с дефиса (отрицательные числа).
CTX_SETTINGS = {"ignore_unknown_options": True}

app = typer.Typer(
    name="toolkit",
    help="Консольный набор утилит: калькулятор и конвертер величин.",
)


@app.command(
    help="Вычислить математическое выражение",
    context_settings=CTX_SETTINGS,
)
def calc(
    expression: str = typer.Argument(..., help="Выражение для вычисления"),
) -> None:
    # calculator
    try:
        result = calculate(expression)
        typer.echo(result)

        # Сохраняем в историю только успешные вычисления
        save_to_history(expression, result)  # <-- ДОБАВЛЕНО

    except ToolkitError as e:
        typer.secho(f"Ошибка: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from e
    except Exception as e:
        typer.secho(f"Непредвиденная ошибка: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from e


@app.command(
    name="convert",
    help="Конвертировать величину",
    context_settings=CTX_SETTINGS,
)
def convert_cmd(
    value: str = typer.Argument(..., help="Числовое значение"),
    from_unit: str = typer.Option(..., "--from", help="Исходная единица"),
    to_unit: str = typer.Option(..., "--to", help="Целевая единица"),
) -> None:
    # Команда конвертер
    try:
        # Парсим строку в число вручную
        try:
            num_value = float(value)
        except ValueError as exc:
            raise InvalidNumberError(f"Неверное числовое значение: {value}") from exc

        result = convert(num_value, from_unit, to_unit)
        typer.echo(result)
    except ToolkitError as e:
        typer.secho(f"Ошибка: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from e
    except Exception as e:
        typer.secho(f"Непредвиденная ошибка: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=2) from e


def main() -> int:
    # Главная функция для запуска через python -m toolkit
    try:
        app()
        return 0
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 0


if __name__ == "__main__":
    sys.exit(main())
