# Project: Python Directory Copier with Gitignore-like Exclusion

## Overview

This project is a Python utility that recursively copies files and directories from a source folder to a destination folder while preserving the directory structure. Each folder can include an `.ignorecopy` file with patterns (similar to a simplified `.gitignore`) to exclude certain files and folders. The script supports options to override these exclusions, display progress as a progress bar (using the `tqdm` library), and print detailed messages in verbose mode. Additionally, it will support an installation option to deploy the script system-wide as a Python package.

## Requirements

- **Primary Functionality:**  
  - Recursively copy files from a source directory to a destination directory.
  - Recreate the folder hierarchy exactly.
  - Read `.ignorecopy` files to avoid copying files/folders that match specified patterns.

- **Command-Line Arguments:**  
  1. Source directory (positional argument).
  2. Destination directory (positional argument).
  3. `--ignore-copy`: Override `.ignorecopy` filtering (copy every file).
  4. `--verbose`: Display detailed output about each copy operation.
  5. `--install`: Optional installation flag to install as a Python Package

- **User Experience Enhancements:**  
  - Use `argparse` for command-line processing.
  - Employ `tqdm` for an elegant terminal-based progress bar.
  - Utilize Python’s robust exception handling for better error management.
  - Modular design to allow for unit testing and future extensions.

## Architecture and Modules

1. **Argument Parser Module:**  
   - Uses `argparse` to capture source and destination paths along with optional flags.

2. **File Filtering Module:**  
   - Reads and parses `.ignorecopy` files.
   - Uses Python’s `fnmatch` for simple wildcard filtering similar to gitignore.

3. **Copy Module:**  
   - Recursively traverses the source directory using `os.walk`.
   - Applies filtering rules and copies files while preserving the folder structure with `shutil.copy2`.

4. **Progress Indicator Module:**  
   - Counts the eligible files and uses `tqdm` to display progress as files are copied.

5. **Installer Module:**  
   - Provides an installation option that install the module as Python Package and assigns the necessary executable permissions.

## Considerations

- **Error Handling:**  
  If an error occurs (e.g., permission issues or file not found), the script will log the error and continue.

- **Compability**
  This script/module has to work in both Windows and Linux.
  
- **Testing & Extensibility:**  
  A modular design easing the development of unit tests (e.g., using `unittest` or `pytest`), along with potential enhancements like dry-run mode or logging capabilities.