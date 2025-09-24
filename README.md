# backup-py-projects

A Python utility for recursively copying directory structures with `.ignorecopy` exclusions, similar to `.gitignore`. Perfect for backing up Python projects while respecting exclusion patterns.

## Features

- **Recursive Directory Copying**: Preserves complete folder hierarchies
- **Exclusion Support**: Uses `.ignorecopy` files with glob patterns (like `.gitignore`)
- **Progress Tracking**: Beautiful progress bars with `tqdm`
- **Verbose Mode**: Detailed operation messages
- **Override Option**: Bypass exclusions with `--ignore-copy` flag
- **Cross-Platform**: Works on Windows and Linux
- **Global Installation**: Install once, use anywhere

## Installation

### Option 1: Global Installation (Recommended)

Install the tool globally using `uv`:

```bash
uv tool install git+https://github.com/tnordal/backup-py-projects.git
```

This installs `backup-py-projects` as a system-wide command. After installation, restart your terminal or run `uv tool update-shell` to update your PATH.

### Option 2: Local Development Installation

For development or local use:

```bash
# Clone the repository
git clone https://github.com/tnordal/backup-py-projects.git
cd backup-py-projects

# Install with development dependencies
uv sync --dev

# Run the tool
uv run backup-py-projects --help
```

## Usage

### Basic Usage

```bash
backup-py-projects /path/to/source /path/to/destination
```

### Options

- `--verbose`: Show detailed operation messages
- `--ignore-copy`: Override `.ignorecopy` filtering (copy everything)

### Examples

```bash
# Basic copy
backup-py-projects ~/projects/my-app ~/backups/my-app

# With verbose output
backup-py-projects ~/projects/my-app ~/backups/my-app --verbose

# Override exclusions (copy everything)
backup-py-projects ~/projects/my-app ~/backups/my-app --ignore-copy
```

## .ignorecopy Files

Create `.ignorecopy` files in any directory to exclude files/folders from copying. Uses the same syntax as `.gitignore`:

```
# Build artifacts
__pycache__/
*.pyc
*.pyo

# Logs
*.log
logs/

# IDE files
.vscode/
.idea/

# OS files
.DS_Store
Thumbs.db
```

Patterns are applied hierarchically - child directory `.ignorecopy` files can override parent patterns.

## Requirements

- Python 3.13+
- `tqdm` (automatically installed)

## Development

```bash
# Install development dependencies
uv sync --dev

# Run tests
uv run pytest

# Lint code
uv run ruff check

# Format code
uv run ruff format
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run `uv run ruff check && uv run ruff format`
6. Submit a pull request

## Support

- **Issues**: [GitHub Issues](https://github.com/tnordal/backup-py-projects/issues)
- **Repository**: [GitHub Repository](https://github.com/tnordal/backup-py-projects)

## Changelog

### v0.2.0
- Removed `--install` CLI flag (global installation now handled via `uv tool install`)
- Added comprehensive README.md with installation and usage documentation
- Added MIT license
- Improved project documentation and setup

### v0.1.0
- Initial release
- Recursive directory copying with `.ignorecopy` support
- Progress bars and verbose mode
- Cross-platform compatibility
- Global installation support