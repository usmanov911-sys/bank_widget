import os
from pathlib import Path
import pytest
from src.decorators import log


@pytest.fixture(scope="function")
def tmp_log_file(tmp_path: Path) -> str:
    """
    Эта фикстура создаёт временный файл для каждого теста,
    чтобы они не мешали друг другу.
    """
    return str(tmp_path / "log.txt")


def test_log_to_console(capsys: pytest.CaptureFixture[str]) -> None:
    """
    Тестируем вывод в консоль.
    """

    @log()
    def my_function(x: int) -> int:
        return x + 10

    result = my_function(5)

    assert result == 15

    captured = capsys.readouterr()
    output_lines = captured.out.splitlines()

    assert len(output_lines) >= 2

    found_ok = any("my_function ok" in line for line in output_lines)
    assert found_ok, "Не найдено сообщения об успешном завершении."


def test_log_to_file(tmp_log_file: str) -> None:
    """
    Тестируем запись в файл.
    """

    @log(filename=tmp_log_file)
    def another_function(a: int, b: float) -> dict[str, Any]:
        return {"result": a * b}

    result = another_function(7, 3.5)

    assert result["result"] == 24.5

    assert os.path.exists(tmp_log_file)

    with open(tmp_log_file, encoding="utf-8") as f:
        content = f.read()

    assert "another_function started" in content
    assert "another_function ok" in content


def test_log_catches_errors(tmp_log_file: str) -> None:
    """
    Тестируем обработку исключений.
    """

    @log(filename=tmp_log_file)
    def failing_function(value: int) -> None:
        if value < 0:
            raise ValueError("Negative input!")

    with pytest.raises(ValueError):
        failing_function(-1)

    with open(tmp_log_file, encoding="utf-8") as f:
        content = f.read()

    assert "failing_function error:" in content
    assert "ValueError" in content
    assert "(args=(-1,)" in content 
