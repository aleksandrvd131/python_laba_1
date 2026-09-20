import argparse
import sys

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import ToolkitError


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="Консольный набор утилит: калькулятор и конвертер величин.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    # Команда calc
    calc_parser = subparsers.add_parser(
        "calc", help="Вычислить математическое выражение"
    )
    calc_parser.add_argument("expression", type=str, help="Выражение для вычисления")

    # Команда convert
    convert_parser = subparsers.add_parser("convert", help="Конвертировать величину")
    convert_parser.add_argument("value", type=float, help="Числовое значение")
    convert_parser.add_argument(
        "--from", dest="from_unit", required=True, help="Исходная единица измерения"
    )
    convert_parser.add_argument(
        "--to", dest="to_unit", required=True, help="Целевая единица измерения"
    )

    args = parser.parse_args()

    # Если что-то не то, то даем хелп
    if args.command is None:
        parser.print_help()
        return 0

    try:
        if args.command == "calc":
            result = calculate(args.expression)
            print(result)
            return 0

        if args.command == "convert":
            result = convert(args.value, args.from_unit, args.to_unit)
            print(result)
            return 0

    except ToolkitError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 2

    except Exception as e:
        print(f"Непредвиденная ошибка: {e}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
