"""
File filtering module for backup-py-projects.

Handles .ignorecopy file parsing and glob pattern matching.
"""

import fnmatch
from pathlib import Path
from typing import Set


class IgnoreCopyFilter:
    """Handles .ignorecopy file parsing and pattern matching."""

    def __init__(self):
        """Initialize the filter with empty pattern sets."""
        self.patterns: Set[str] = set()
        self.directory_patterns: Set[str] = set()

    def load_ignorecopy_file(self, ignorecopy_path: Path) -> None:
        """
        Load patterns from an .ignorecopy file.

        Args:
            ignorecopy_path: Path to the .ignorecopy file
        """
        if not ignorecopy_path.exists() or not ignorecopy_path.is_file():
            return

        try:
            with open(ignorecopy_path, "r", encoding="utf-8") as f:
                for line in f:
                    pattern = line.strip()

                    # Skip empty lines and comments
                    if not pattern or pattern.startswith("#"):
                        continue

                    # Remove leading slash if present (gitignore compatibility)
                    if pattern.startswith("/"):
                        pattern = pattern[1:]

                    # Directory patterns (ending with /)
                    if pattern.endswith("/"):
                        self.directory_patterns.add(pattern[:-1])
                    else:
                        self.patterns.add(pattern)

        except (OSError, UnicodeDecodeError):
            # Silently ignore errors reading .ignorecopy files
            pass

    def should_ignore_file(self, file_path: Path, relative_to: Path) -> bool:
        """
        Check if a file should be ignored based on loaded patterns.

        Args:
            file_path: Full path to the file
            relative_to: Base path to calculate relative path from

        Returns:
            bool: True if file should be ignored, False otherwise
        """
        if not self.patterns:
            return False

        try:
            # Get relative path from base directory
            rel_path = file_path.relative_to(relative_to)
            rel_path_str = str(rel_path).replace("\\", "/")  # Normalize separators
            filename = file_path.name

            # Check against all patterns
            for pattern in self.patterns:
                # Check full relative path
                if fnmatch.fnmatch(rel_path_str, pattern):
                    return True

                # Check just filename
                if fnmatch.fnmatch(filename, pattern):
                    return True

                # Check if any parent directory matches
                for parent in rel_path.parents:
                    parent_str = str(parent).replace("\\", "/")
                    if fnmatch.fnmatch(parent_str, pattern):
                        return True

        except ValueError:
            # file_path is not relative to relative_to
            return False

        return False

    def should_ignore_directory(self, dir_path: Path, relative_to: Path) -> bool:
        """
        Check if a directory should be ignored based on loaded patterns.

        Args:
            dir_path: Full path to the directory
            relative_to: Base path to calculate relative path from

        Returns:
            bool: True if directory should be ignored, False otherwise
        """
        if not self.patterns and not self.directory_patterns:
            return False

        try:
            # Get relative path from base directory
            rel_path = dir_path.relative_to(relative_to)
            rel_path_str = str(rel_path).replace("\\", "/")  # Normalize separators
            dirname = dir_path.name

            # Check against directory-specific patterns
            for pattern in self.directory_patterns:
                if fnmatch.fnmatch(rel_path_str, pattern):
                    return True
                if fnmatch.fnmatch(dirname, pattern):
                    return True

            # Check against general patterns
            for pattern in self.patterns:
                if fnmatch.fnmatch(rel_path_str, pattern):
                    return True
                if fnmatch.fnmatch(dirname, pattern):
                    return True

        except ValueError:
            # dir_path is not relative to relative_to
            return False

        return False

    def clear_patterns(self) -> None:
        """Clear all loaded patterns."""
        self.patterns.clear()
        self.directory_patterns.clear()


class FilterManager:
    """Manages filtering across directory tree with hierarchical .ignorecopy files."""

    def __init__(self, base_path: Path, ignore_filters: bool = False):
        """
        Initialize the filter manager.

        Args:
            base_path: Base directory path for the copy operation
            ignore_filters: If True, ignore all filtering (copy everything)
        """
        self.base_path = base_path
        self.ignore_filters = ignore_filters
        self.filter_cache: dict[Path, IgnoreCopyFilter] = {}

    def get_filter_for_directory(self, directory: Path) -> IgnoreCopyFilter:
        """
        Get the appropriate filter for a directory, loading .ignorecopy files
        from the directory hierarchy.

        Args:
            directory: Directory to get filter for

        Returns:
            IgnoreCopyFilter: Filter with patterns loaded from hierarchy
        """
        if self.ignore_filters:
            # Return empty filter when ignoring all filters
            return IgnoreCopyFilter()

        # Check cache first
        if directory in self.filter_cache:
            return self.filter_cache[directory]

        # Create new filter and load patterns from hierarchy
        combined_filter = IgnoreCopyFilter()

        # Collect all .ignorecopy files from base_path to current directory
        current_path = directory
        ignorecopy_files = []

        while current_path >= self.base_path:
            ignorecopy_file = current_path / ".ignorecopy"
            if ignorecopy_file.exists():
                ignorecopy_files.append(ignorecopy_file)

            if current_path == self.base_path:
                break
            current_path = current_path.parent

        # Merge patterns from all .ignorecopy files
        for ignorecopy_file in reversed(ignorecopy_files):
            combined_filter.load_ignorecopy_file(ignorecopy_file)

        # Cache the combined filter
        self.filter_cache[directory] = combined_filter
        return combined_filter

    def should_ignore_file(self, file_path: Path) -> bool:
        """
        Check if a file should be ignored based on .ignorecopy files in its hierarchy.

        Args:
            file_path: Path to the file

        Returns:
            bool: True if file should be ignored
        """
        if self.ignore_filters:
            return False

        filter_obj = self.get_filter_for_directory(file_path.parent)
        return filter_obj.should_ignore_file(file_path, self.base_path)

    def should_ignore_directory(self, dir_path: Path) -> bool:
        """
        Check if a directory should be ignored based on .ignorecopy files in its hierarchy.

        Args:
            dir_path: Path to the directory

        Returns:
            bool: True if directory should be ignored
        """
        if self.ignore_filters:
            return False

        # Check with parent's filter (since directory might not exist in cache yet)
        parent_filter = self.get_filter_for_directory(dir_path.parent)
        return parent_filter.should_ignore_directory(dir_path, self.base_path)
