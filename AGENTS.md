# Project Name: Nariah’s Chuck Norris Jokes CLI

## Overview
A command-line tool to fetch and display Chuck Norris jokes from the public Chuck Norris API.  
Users can get random jokes, browse categories, search jokes by keyword, and optionally get a random joke from a specific category.

This project is designed to be AI-assisted, meaning tools like ChatGPT, Copilot, and Gemini can use this file as context when helping extend, debug, or refactor the code.

---

## API Integration
- **API:** Chuck Norris Jokes API
- **Base URL:** https://api.chucknorris.io
- **Key endpoints:**
  - `/jokes/random`  
    - Get a single random joke  
    - Optional query param: `?category={category}`
  - `/jokes/categories`  
    - Get a list of available categories
  - `/jokes/search?query={term}`  
    - Search for jokes containing a keyword
- **Data format:** JSON objects and arrays  
  - Random joke: `{ "value": "joke text", ... }`  
  - Search results: `{ "result": [ { "value": "joke text", ... }, ... ] }`  

---

## CLI Commands
Current CLI behavior (in `src/main.py`):

- `python -m src.main random`  
  - Get a single random Chuck Norris joke from any category.

- `python -m src.main random --category <category>`  
  - Get a random joke from a specific category (for example `dev`, `animal`, etc.).

- `python -m src.main categories`  
  - List all available joke categories returned by the API.

- `python -m src.main search "<keyword>"`  
  - Search for jokes containing a given keyword.  
  - Optional flags (depending on implementation): `--limit` to limit number of results.

When asking AI for help, assume these commands must remain stable and user-friendly.

---

## Technical Stack
- **Language:** Python 3.11+  
- **CLI:** `argparse` for command-line argument parsing  
- **HTTP Client:** `requests` for API calls  
- **Testing:** `pytest`  
- **Mocking:** `unittest.mock` (`patch`, `MagicMock`) for mocking API calls  
- **CI/CD:** GitHub Actions workflow in `.github/workflows/tests.yml`

---

## Code Organization
- `src/main.py`  
  - Entry point and `argparse` setup.  
  - Parses commands (`random`, `categories`, `search`, etc.) and calls functions from `api.py`.  
  - Responsible for printing user-facing output and handling user input.

- `src/api.py`  
  - API interaction functions for the Chuck Norris API.  
  - Contains:
    - `get_random_joke()`
    - `get_categories()`
    - `get_random_from_category(category: str)`
    - `search_jokes(query: str, limit: int = 5)`
    - `_handle_response(response)` for centralized response/error handling.
  - Raises `ChuckAPIError` for any API-related problems.

- `src/__init__.py`  
  - Marks `src` as a package. Usually minimal.

- `tests/test_api.py`  
  - Tests `src.api` functions using `pytest` and `unittest.mock`.  
  - All external HTTP calls (via `requests.get`) are mocked so tests never hit the real API.

- `tests/test_main.py`  
  - Tests CLI behavior (argument parsing and wiring) using `pytest`.  
  - Verifies that the correct API functions are called and that output is as expected.

- `.github/workflows/tests.yml`  
  - GitHub Actions workflow that installs dependencies and runs `pytest` on each push/pull request.

---

## Standards
- Use descriptive function names and **docstrings** for all public functions and classes.
- Follow **PEP 8** style guidelines (naming, spacing, imports, line length where reasonable).
- Handle errors gracefully with `try/except` blocks, especially around:
  - Network errors (`requests` exceptions)
  - Invalid JSON
  - Unexpected response formats
- Never call the real API from tests:
  - All API calls in tests must be mocked using `@patch("src.api.requests.get")`.
- Keep user-facing CLI messages clear, friendly, and informative (especially on errors).
- Avoid hardcoding values that might need to change (e.g., base URL defined once as `BASE_URL` in `api.py`).

---

## AI Usage & Prompting Guidelines

This file is meant to help AI tools assist with this project. When I (Nariah) am stuck, I want AI to:

- Explain what’s going wrong in **plain language**.
- Suggest **small, safe changes** instead of rewriting everything.
- Help with **debugging tests**, especially mocking and CI failures.
- Help me think through **next steps** if I do not know what to do.

### When I’m stuck on code logic
Example prompt:
> “Here is my function and the failing test output. Explain why this is failing and suggest a minimal change to fix it:  
> \- Function: [paste from src/api.py or src/main.py]  
> \- Test output: [paste pytest error].”

### When I’m stuck on mocking/API tests
Example prompt:
> “I’m testing a function in `src/api.py` that uses `requests.get`. Show me how to properly mock `requests.get` in `tests/test_api.py` so that no real API calls happen, and the test passes.”

### When I’m stuck on CLI / argparse
Example prompt:
> “My CLI uses `argparse` in `src/main.py` with commands `random`, `categories`, and `search`. I’m getting this error when I run `python -m src.main search coffee`: [paste error]. Help me fix the argparse setup without changing the overall command names.”

### When I’m stuck on GitHub Actions / CI failing
Example prompt:
> “My tests pass locally but fail in GitHub Actions. Here’s my `.github/workflows/tests.yml` and the CI error: [paste both]. Explain what’s wrong and how to fix it.”

### When I don’t know what to do next
Example prompt:
> “Here is the current state of my project (summarized). I want to strengthen it for grading and for my portfolio. Suggest 2–3 small improvements I can make next that would give me the biggest impact.”

---

## Goals for Future Improvements
If I decide to extend this project later, good ideas for AI to help with:

- Adding a command to **save favorite jokes** to a local file.
- Adding a command to **format output nicely** (e.g., colored text or borders).
- Adding **more robust error messages**, such as:
  - Handling no search results.
  - Letting the user know if a category doesn’t exist.
- Refactoring `src/main.py` to be even more modular and easier to test.

AI tools should respect this structure and style, and help evolve the project without breaking the existing commands or tests.
