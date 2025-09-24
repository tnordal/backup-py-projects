"""
Backup Python Projects - A utility for copying directory structures.

Main entry point for the CLI application.
"""

from .cli import parse_arguments, validate_paths
from .copier import DirectoryCopier


def hello() -> str:
    """Legacy hello function for compatibility."""
    return "Hello from backup-py-projects!"


def main() -> None:
    """
    Main entry point for the backup-py-projects CLI.

    Parses arguments, validates paths, and executes the copy operation.
    """
    # Parse command-line arguments
    args = parse_arguments()

    # Validate source and destination paths
    source_path, dest_path = validate_paths(args.source, args.destination)

    # Create copier instance and execute copy operation
    copier = DirectoryCopier(source_path, dest_path, args.verbose)
    success = copier.copy_directory(ignore_filters=args.ignore_copy)

    # Exit with appropriate code
    if not success:
        exit(1)
