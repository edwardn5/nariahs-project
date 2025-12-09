# Nariahs Project – Chuck Norris Jokes CLI

## Overview

This repository contains a Python command-line interface (CLI) that uses the public Chuck Norris API (https://api.chucknorris.io/) to fetch and display jokes. The goal is to demonstrate an AI-assisted development workflow for a midterm project: designing a CLI, integrating a public API, writing tests, and setting up CI with GitHub Actions.

The primary user is **Nariah**, a college student building this as a portfolio-ready project and graded midterm.

---

## Project Goals

- Build a CLI with at least **3 commands** using `argparse`.
- Integrate with a **no-auth public API** (Chuck Norris).
- Write tests with **pytest** and mocking (no real HTTP requests in tests).
- Configure a **GitHub Actions** workflow to run tests on each push/PR.
- Document AI usage and project context in this `AGENTS.md` file.
- Produce a clean, readable codebase that is easy to run and grade.

---

## API Details

- **API Name:** Chuck Norris Jokes API  
- **Base URL:** `https://api.chucknorris.io`

Key endpoints used:

- `GET /jokes/random`  
  - Returns a random joke.  
- `GET /jokes/random?category={category}`  
  - Returns a random joke from the given category.  
- `GET /jokes/categories`  
  - Returns a list of available categories.  
- `GET /jokes/search?query={query}`  
  - Returns jokes that match the search query.

API responses are JSON. For jokes, the key field is usually `value` (the joke text). For search, there is a `result` list of joke objects.

---

## CLI Commands

The CLI entry point is `src/main.py` and is run with:

```bash
python -m src.main <command> [options]

