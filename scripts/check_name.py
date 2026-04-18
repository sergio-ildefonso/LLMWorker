"""Check if a package name is available on PyPI."""

from __future__ import annotations

import argparse
import sys

import requests


def is_name_available(package_name: str) -> bool:
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url, timeout=10)
    if response.status_code == 404:
        return True
    if response.status_code == 200:
        return False
    response.raise_for_status()
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Check PyPI package-name availability.")
    parser.add_argument("name", help="Package name to check on PyPI")
    args = parser.parse_args()

    try:
        available = is_name_available(args.name)
    except requests.RequestException as exc:
        print(f"Error checking '{args.name}': {exc}", file=sys.stderr)
        return 2

    if available:
        print(f"AVAILABLE: '{args.name}' does not exist on PyPI.")
        return 0

    print(f"TAKEN: '{args.name}' already exists on PyPI.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
