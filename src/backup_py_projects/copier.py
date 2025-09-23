"""
Core copying functionality for backup-py-projects.

Handles recursive directory traversal and file copying operations.
"""

import os
import shutil
import sys
from pathlib import Path

from .progress import ProgressTracker


class DirectoryCopier:
    """Handles recursive directory copying with filtering support."""

    def __init__(self, source: Path, destination: Path, verbose: bool = False):
        """
        Initialize the directory copier.

        Args:
            source: Source directory path
            destination: Destination directory path
            verbose: Whether to display detailed output
        """
        self.source = source
        self.destination = destination
        self.verbose = verbose
        self.files_copied = 0
        self.errors: list[str] = []

    def copy_directory(self, ignore_filters: bool = False) -> bool:
        """
        Copy the entire directory structure from source to destination.

        Args:
            ignore_filters: If True, ignore .ignorecopy files and copy everything

        Returns:
            bool: True if copy operation completed, False if critical errors occurred
        """
        if self.verbose:
            print(f"Copying from: {self.source}")
            print(f"Copying to: {self.destination}")

        # Count total files for progress tracking
        total_files = self._count_files(ignore_filters)

        if total_files == 0:
            print("No files to copy.")
            return True

        # Initialize progress tracker
        progress = ProgressTracker(total_files, self.verbose)

        try:
            self._copy_recursive(
                self.source, self.destination, ignore_filters, progress
            )
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return False
        except Exception as e:
            print(f"Critical error during copy operation: {e}", file=sys.stderr)
            return False
        finally:
            progress.close()

        # Print summary
        print(f"\nCopy completed: {self.files_copied} files copied")
        if self.errors:
            print(f"Errors encountered: {len(self.errors)}")
            if self.verbose:
                for error in self.errors:
                    print(f"  Error: {error}")

        return True

    def _count_files(self, ignore_filters: bool) -> int:
        """
        Count the total number of files that will be copied.

        Args:
            ignore_filters: Whether to ignore filtering rules

        Returns:
            int: Total number of files to be copied
        """
        count = 0
        for root, dirs, files in os.walk(self.source):
            # TODO: Apply filtering logic here when filters module is implemented
            count += len(files)
        return count

    def _copy_recursive(
        self,
        current_source: Path,
        current_dest: Path,
        ignore_filters: bool,
        progress: ProgressTracker,
    ) -> None:
        """
        Recursively copy files and directories.

        Args:
            current_source: Current source directory being processed
            current_dest: Current destination directory
            ignore_filters: Whether to ignore filtering rules
            progress: Progress tracker instance
        """
        try:
            # Ensure destination directory exists
            current_dest.mkdir(parents=True, exist_ok=True)

            # Process all items in current directory
            for item in current_source.iterdir():
                dest_item = current_dest / item.name

                if item.is_file():
                    self._copy_file(item, dest_item, progress)
                elif item.is_dir():
                    # Recursively copy subdirectory
                    self._copy_recursive(item, dest_item, ignore_filters, progress)

        except PermissionError as e:
            error_msg = f"Permission denied accessing '{current_source}': {e}"
            self.errors.append(error_msg)
            if self.verbose:
                print(f"Warning: {error_msg}")

    def _copy_file(
        self, source_file: Path, dest_file: Path, progress: ProgressTracker
    ) -> None:
        """
        Copy a single file from source to destination.

        Args:
            source_file: Source file path
            dest_file: Destination file path
            progress: Progress tracker instance
        """
        try:
            # Use shutil.copy2 to preserve metadata
            shutil.copy2(source_file, dest_file)
            self.files_copied += 1

            if self.verbose:
                progress.update_with_message(f"Copied: {source_file.name}")
            else:
                progress.update()

        except PermissionError as e:
            error_msg = f"Permission denied copying '{source_file}': {e}"
            self.errors.append(error_msg)
            progress.update()  # Still update progress even on error

        except OSError as e:
            error_msg = f"OS error copying '{source_file}': {e}"
            self.errors.append(error_msg)
            progress.update()  # Still update progress even on error
