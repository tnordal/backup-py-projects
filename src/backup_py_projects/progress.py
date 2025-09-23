"""
Progress tracking module for backup-py-projects.

Provides progress bar functionality using tqdm.
"""

from tqdm import tqdm


class ProgressTracker:
    """Manages progress tracking and display during copy operations."""

    def __init__(self, total: int, verbose: bool = False):
        """
        Initialize the progress tracker.

        Args:
            total: Total number of items to process
            verbose: Whether to show detailed progress messages
        """
        self.total = total
        self.verbose = verbose
        self.current = 0

        # Initialize tqdm progress bar
        self.pbar = tqdm(
            total=total,
            desc="Copying files",
            unit="files",
            disable=verbose,  # Disable progress bar in verbose mode
        )

    def update(self, amount: int = 1) -> None:
        """
        Update the progress counter.

        Args:
            amount: Number of items to add to progress (default: 1)
        """
        self.current += amount
        if not self.verbose:
            self.pbar.update(amount)

    def update_with_message(self, message: str, amount: int = 1) -> None:
        """
        Update progress and display a message (for verbose mode).

        Args:
            message: Message to display
            amount: Number of items to add to progress (default: 1)
        """
        self.current += amount

        if self.verbose:
            # In verbose mode, print the message directly
            print(f"[{self.current}/{self.total}] {message}")
        else:
            # In non-verbose mode, update progress bar with message
            self.pbar.set_postfix_str(message)
            self.pbar.update(amount)

    def close(self) -> None:
        """Close the progress bar and clean up resources."""
        if hasattr(self, "pbar"):
            self.pbar.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
