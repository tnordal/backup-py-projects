"""
Command-line interface module for backup-py-projects.

Handles argument parsing and CLI entry point.
"""

import argparse
import sys
from pathlib import Path


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the backup utility.

    Returns:
        argparse.Namespace: Parsed arguments containing source, destination,
            and optional flags.
    """
    parser = argparse.ArgumentParser(
        prog="backup-py-projects",
        description="Copy directory structures with .ignorecopy exclusions",
    )

    # Positional arguments
    parser.add_argument("source", type=str, help="Source directory to copy from")

    parser.add_argument(
        "destination", type=str, help="Destination directory to copy to"
    )

    # Optional flags
    parser.add_argument(
        "--ignore-copy",
        action="store_true",
        help="Override .ignorecopy filtering (copy everything)",
    )

    parser.add_argument(
        "--verbose", action="store_true", help="Display detailed operation messages"
    )

    parser.add_argument(
        "--install", action="store_true", help="Install as a system-wide Python package"
    )

    return parser.parse_args()


def validate_paths(source: str, destination: str) -> tuple[Path, Path]:
    """
    Validate and convert source and destination paths.

    Args:
        source: Source directory path string
        destination: Destination directory path string

    Returns:
        tuple[Path, Path]: Validated source and destination Path objects

    Raises:
        SystemExit: If validation fails
    """
    source_path = Path(source).resolve()
    destination_path = Path(destination).resolve()

    # Check if source exists and is a directory
    if not source_path.exists():
        print(
            f"Error: Source directory '{source_path}' does not exist", file=sys.stderr
        )
        sys.exit(1)

    if not source_path.is_dir():
        print(f"Error: Source '{source_path}' is not a directory", file=sys.stderr)
        sys.exit(1)

    # Create destination directory if it doesn't exist
    try:
        destination_path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print(
            f"Error: Cannot create destination directory '{destination_path}'",
            file=sys.stderr,
        )
        sys.exit(1)

    return source_path, destination_path
