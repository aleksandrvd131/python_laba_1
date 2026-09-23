import json
from pathlib import Path

import pytest
from toolkit.history import HISTORY_FILE, load_history, save_to_history


def test_save_to_history_creates_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Проверяет, что файл создаётся при первой записи."""
    monkeypatch.chdir(tmp_path)

    save_to_history("2 + 2", 4.0)

    assert HISTORY_FILE.exists()


def test_save_to_history_json_format(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Проверяет, что JSON имеет правильный формат."""
    monkeypatch.chdir(tmp_path)

    save_to_history("10 / 2", 5.0)

    with HISTORY_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["expression"] == "10 / 2"
    assert data[0]["result"] == 5.0
    assert "timestamp" in data[0]


def test_save_to_history_accumulates(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Проверяет, что история накапливается."""
    monkeypatch.chdir(tmp_path)

    save_to_history("2 + 2", 4.0)
    save_to_history("3 * 3", 9.0)
    save_to_history("10 - 5", 5.0)

    history = load_history()

    assert len(history) == 3
    assert history[0]["expression"] == "2 + 2"
    assert history[1]["expression"] == "3 * 3"
    assert history[2]["expression"] == "10 - 5"


def test_load_history_empty(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Проверяет, что без файла история пустая."""
    monkeypatch.chdir(tmp_path)

    history = load_history()

    assert history == []


def test_load_history_corrupted_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Проверяет, что повреждённый JSON не вызывает ошибку."""
    monkeypatch.chdir(tmp_path)

    HISTORY_FILE.write_text("это не JSON", encoding="utf-8")

    history = load_history()

    assert history == []
