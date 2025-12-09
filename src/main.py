"""
Command-line interface for the Chuck Norris Jokes CLI application.

Run with:
    python -m src.main <command> [options]
"""

from __future__ import annotations

import argparse
from typing import List

from . import api


def _print_jokes(jokes: List[str]) -> None:
    """
    Print one or more jokes with simple formatting.

    Parameters
    ----------
    jokes : List[str]
        List of joke strings to print.
    """
    if not jokes:
        print("No jokes found.")
        return

    if len(jokes) == 1:
        print(jokes[0])
        return

    for idx, joke in enumerate(jokes, start=1):
        print(f"[{idx}] {joke}")
        print("-" * 40)


def random_command(args: argparse.Namespace) -> None:
    """Handle the 'random' subcommand."""
    try:
        if args.category:
            joke = api.get_random_from_category(args.category)
        else:
            joke = api.get_random_joke()
        _print_jokes([joke])
    except api.ChuckAPIError as exc:
        print(f"Error: {exc}")


def categories_command(_args: argparse.Namespace) -> None:
    """Handle the 'categories' subcommand."""
    try:
        categories = api.get_categories()
        if not categories:
            print("No categories found.")
            return
        print("Available categories:")
        for cat in categories:
            print(f"- {cat}")
    except api.ChuckAPIError as exc:
        print(f"Error: {exc}")


def search_command(args: argparse.Namespace) -> None:
    """Handle the 'search' subcommand."""
    try:
        jokes = api.search_jokes(args.query, limit=args.limit)
        _print_jokes(jokes)
    except api.ChuckAPIError as exc:
        print(f"Error: {exc}")


def build_parser() -> argparse.ArgumentParser:
    """
    Build and return the top-level argument parser.

    Returns
    -------
    argparse.ArgumentParser
        Configured parser instance.
    """
    parser = argparse.ArgumentParser(
        description="Nariahs Project – Chuck Norris Jokes CLI powered by https://api.chucknorris.io/"
    )

    subparsers = parser.add_subparsers(
        title="Commands",
        dest="command",
        required=True,
        help="Available commands",
    )

    # random
    random_parser = subparsers.add_parser(
        "random",
        help="Get a random Chuck Norris joke, optionally by category.",
    )
    random_parser.add_argument(
        "-c",
        "--category",
        help="Category to get a random joke from (optional).",
        type=str,
    )
    random_parser.set_defaults(func=random_command)

    # categories
    categories_parser = subparsers.add_parser(
        "categories",
        help="List all available joke categories.",
    )
    categories_parser.set_defaults(func=categories_command)

    # search
    search_parser = subparsers.add_parser(
        "search",
        help="Search for jokes containing a given word or phrase.",
    )
    search_parser.add_argument(
        "query",
        help="Search query string.",
        type=str,
    )
    search_parser.add_argument(
        "-l",
        "--limit",
        help="Maximum number of results to show (default: 5).",
        type=int,
        default=5,
    )
    search_parser.set_defaults(func=search_command)

    return parser


def main(argv: list[str] | None = None) -> None:
    """
    Entry point for the CLI.

    Parameters
    ----------
    argv : list[str] | None, optional
        Optional list of arguments, useful for testing.
        If None, uses sys.argv.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()

