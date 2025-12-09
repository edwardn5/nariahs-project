"""
Tests for the CLI layer in src.main.
"""

from __future__ import annotations

from unittest.mock import patch

from src import main


@patch("src.main.api.get_random_joke", return_value="random joke")
def test_random_command_no_category(mock_random, capsys) -> None:
    main.main(["random"])
    captured = capsys.readouterr()
    assert "random joke" in captured.out
    mock_random.assert_called_once()


@patch("src.main.api.get_random_from_category", return_value="dev joke")
def test_random_command_with_category(mock_dev, capsys) -> None:
    main.main(["random", "--category", "dev"])
    captured = capsys.readouterr()
    assert "dev joke" in captured.out
    mock_dev.assert_called_once_with("dev")


@patch("src.main.api.get_categories", return_value=["dev", "movie"])
def test_categories_command(mock_cats, capsys) -> None:
    main.main(["categories"])
    captured = capsys.readouterr()
    out = captured.out
    assert "Available categories:" in out
    assert "- dev" in out
    assert "- movie" in out
    mock_cats.assert_called_once()


@patch("src.main.api.search_jokes", return_value=["j1", "j2"])
def test_search_command(mock_search, capsys) -> None:
    main.main(["search", "coffee", "--limit", "2"])
    captured = capsys.readouterr()
    out = captured.out
    assert "[1] j1" in out
    assert "[2] j2" in out
    mock_search.assert_called_once_with("coffee", limit=2)
