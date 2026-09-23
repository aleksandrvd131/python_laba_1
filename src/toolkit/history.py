"""Модуль для работы с историей вычислений."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

# Путь к файлу истории (создаётся в текущей директории)
HISTORY_FILE = Path("history.json")


def load_history() -> list[dict[str, Any]]:
    """Загружает историю вычислений из JSON-файла.

    Returns:
        Список записей истории. Если файла нет или он повреждён,
        возвращает пустой список.
    """
    if not HISTORY_FILE.exists():
        return []

    try:
        with HISTORY_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        # Если файл повреждён, возвращаем пустую историю
        return []


def save_to_history(expression: str, result: float) -> None:
    """Сохраняет успешное вычисление в историю.

    Args:
        expression: Исходное выражение.
        result: Результат вычисления.
    """
    # Загружаем существующую историю
    history = load_history()

    # Создаём новую запись
    entry = {
        "expression": expression,
        "result": result,
        "timestamp": datetime.now().isoformat(),
    }

    # Добавляем запись в историю
    history.append(entry)

    # Записываем всё обратно в файл
    with HISTORY_FILE.open("w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
