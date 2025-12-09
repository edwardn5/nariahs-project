"""
API integration for the Chuck Norris Jokes CLI.

This module provides helper functions to interact with the
https://api.chucknorris.io/ public API.
"""

from __future__ import annotations

from typing import List
import requests


BASE_URL = "https://api.chucknorris.io"


class ChuckAPIError(Exception):
    """Custom exception for Chuck Norris API related errors."""


def _handle_response(response: requests.Response) -> dict:
    """
    Validate an HTTP response and return its JSON content.

    Raises
    ------
    ChuckAPIError
        If the response status code is not 200 or JSON decoding fails.
    """
    try:
        # This may raise requests.HTTPError OR a generic Exception (in tests we mock it).
        response.raise_for_status()
    except Exception as exc:
        # Catch ANY error from raise_for_status and wrap it in ChuckAPIError
        status = getattr(response, "status_code", "unknown")
        raise ChuckAPIError(f"API request failed (status: {status})") from exc

    try:
        return response.json()
    except Exception as exc:
        # Any JSON decoding or unexpected error
        raise ChuckAPIError("Failed to decode JSON from API response") from exc


def get_random_joke() -> str:
    """
    Fetch a random Chuck Norris joke.

    Returns
    -------
    str
        The joke text.
    """
    url = f"{BASE_URL}/jokes/random"
    resp = requests.get(url, timeout=10)
    data = _handle_response(resp)
    return data.get("value", "No joke found.")


def get_categories() -> List[str]:
    """
    Fetch all available Chuck Norris joke categories.

    Returns
    -------
    List[str]
        List of category names.
    """
    url = f"{BASE_URL}/jokes/categories"
    resp = requests.get(url, timeout=10)
    try:
        resp.raise_for_status()
        data = resp.json()
    except (requests.HTTPError, ValueError) as exc:
        raise ChuckAPIError("Failed to fetch categories") from exc

    if not isinstance(data, list):
        raise ChuckAPIError("Unexpected categories response format.")

    return [str(cat) for cat in data]


def get_random_from_category(category: str) -> str:
    """
    Fetch a random joke from a specific category.

    Parameters
    ----------
    category : str
        Name of the category.

    Returns
    -------
    str
        Joke text.
    """
    url = f"{BASE_URL}/jokes/random"
    params = {"category": category}
    resp = requests.get(url, params=params, timeout=10)
    data = _handle_response(resp)
    return data.get("value", "No joke found.")


def search_jokes(query: str, limit: int = 5) -> List[str]:
    """
    Search for jokes that contain a given query string.

    Parameters
    ----------
    query : str
        Search term to look for in jokes.
    limit : int, optional
        Maximum number of jokes to return, by default 5.

    Returns
    -------
    List[str]
        A list of joke strings, up to the specified limit.
    """
    url = f"{BASE_URL}/jokes/search"
    params = {"query": query}
    resp = requests.get(url, params=params, timeout=10)
    data = _handle_response(resp)

    result_list = data.get("result", [])
    jokes = [item.get("value", "") for item in result_list]
    return jokes[:limit]
