# Copilot Instructions: backup-py-projects

## Project Overview
This is a private utility package for backing up Python project folders, built with modern Python tooling (uv, Python 3.13+). The project follows a minimal src-layout structure with strict typing enforcement.

## Architecture & Structure
- **Package Layout**: Uses `src/backup_py_projects/` layout (not flat structure)
- **Entry Point**: CLI command `backup-py-projects` maps to `backup_py_projects:hello` in pyproject.toml
- **Typing**: Strict typing enforced with `py.typed` marker file - all functions must have type hints
- **Python Version**: Requires Python 3.13+ (see `.python-version`)

## Development Workflow

### Environment Setup
```bash
# Use uv for all dependency management (not pip/pipenv/poetry)
uv sync --dev                    # Install dev dependencies
uv add <package>                 # Add runtime dependency  
uv add --dev <package>          # Add dev dependency
```

### Code Quality Tools
- **Linting/Formatting**: Uses `ruff` (configured in pyproject.toml dev group)
- **Testing**: Uses `pytest>=8` for testing framework
- **Build System**: Uses `uv_build` backend (not setuptools/flit)

### Running & Testing
```bash
uv run backup-py-projects       # Run CLI command
uv run pytest                   # Run tests
uv run ruff check               # Lint code
uv run ruff format              # Format code
```

## Code Conventions

### Python Style
- **PEP 8 Compliance**: 4-space indentation, 79 character line limit
- **Type Hints**: Required for all functions, use modern syntax (`list[str]` not `List[str]`)
- **Docstrings**: Follow PEP 257, include parameter and return type documentation
- **Function Names**: Descriptive names with clear intent

### Example Pattern
```python
def backup_project(source_path: str, destination: str) -> bool:
    """
    Back up a Python project to the specified destination.
    
    Args:
        source_path: Path to the source project directory
        destination: Target backup location
        
    Returns:
        True if backup successful, False otherwise
    """
    # Implementation here
```

## Project-Specific Patterns
- **CLI Integration**: Entry points defined in pyproject.toml `[project.scripts]` section
- **Private Package**: Uses `"Private :: Do Not Upload"` classifier to prevent PyPI publishing
- **No External Dependencies**: Runtime dependencies kept minimal (currently none)
- **Dev Dependencies**: All development tools managed through `[dependency-groups]` not `[tool.*]`

## Key Files to Understand
- `pyproject.toml`: Single source of truth for project metadata, dependencies, and tool configuration
- `src/backup_py_projects/__init__.py`: Main module with CLI entry point
- `uv.lock`: Lock file for reproducible builds (like package-lock.json)
- `.python-version`: pyenv-compatible Python version specification