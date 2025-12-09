"""
Tests for src.api using mocked HTTP requests.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src import api


@patch("src.api.requests.get")
def test_get_random_joke_success(mock_get: MagicMock) -> None:
    mock_response = MagicMock()
    mock_response.json.return_value = {"value": "test joke"}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    joke = api.get_random_joke()

    assert joke == "test joke"
    mock_get.assert_called_once()


@patch("src.api.requests.get")
def test_get_categories_success(mock_get: MagicMock) -> None:
    mock_response = MagicMock()
    mock_response.json.return_value = ["dev", "movie"]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    categories = api.get_categories()

    assert categories == ["dev", "movie"]
    mock_get.assert_called_once()


@patch("src.api.requests.get")
def test_search_jokes_limit(mock_get: MagicMock) -> None:
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "result": [
            {"value": "joke 1"},
            {"value": "joke 2"},
            {"value": "joke 3"},
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    jokes = api.search_jokes("test", limit=2)

    assert jokes == ["joke 1", "joke 2"]
    mock_get.assert_called_once()


@patch("src.api.requests.get")
def test_get_random_from_category_error(mock_get: MagicMock) -> None:
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("boom")
    mock_get.return_value = mock_response

    with pytest.raises(api.ChuckAPIError):
        api.get_random_from_category("dev")

