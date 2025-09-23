# Task: Python Directory Copier with Gitignore-like Exclusion

## Project Goal

Create a Python utility that recursively copies files and directories from a source folder to a destination folder while preserving the directory structure. The utility should support `.ignorecopy` files for excluding certain files/folders (similar to `.gitignore`) and provide user-friendly features like progress bars and verbose output.

## Key Requirements

### Core Functionality
1. **Recursive Directory Copying**: Copy files from source to destination while maintaining folder hierarchy
2. **Exclusion Pattern Support**: Use `.ignorecopy` files with glob patterns to exclude files/folders
3. **Structure Preservation**: Recreate the exact folder structure in the destination

### Command-Line Interface
- **Positional Arguments**:
  - Source directory path
  - Destination directory path
- **Optional Flags**:
  - `--ignore-copy`: Override `.ignorecopy` filtering (copy everything)
  - `--verbose`: Display detailed operation messages
  - `--install`: Install as a system-wide Python package

### User Experience Features
- **Progress Bar**: Use `tqdm` for visual progress indication
- **Error Handling**: Robust exception handling with graceful error recovery
- **Cross-Platform**: Support both Windows and Linux

## Technical Architecture

### Module Structure (following src-layout)
```
src/backup_py_projects/
├── __init__.py          # Main CLI entry point
├── py.typed             # Type checking marker
├── cli.py               # Argument parsing module
├── filters.py           # File filtering with .ignorecopy support
├── copier.py            # Core copying functionality
├── progress.py          # Progress tracking with tqdm
└── installer.py         # Package installation utilities
```

### Implementation Modules

1. **CLI Module** (`cli.py`)
   - Use `argparse` for command-line argument processing
   - Handle source/destination validation
   - Process optional flags

2. **Filters Module** (`filters.py`)
   - Read and parse `.ignorecopy` files
   - Use `fnmatch` for glob pattern matching
   - Support gitignore-style pattern syntax

3. **Copier Module** (`copier.py`)
   - Use `os.walk()` for directory traversal
   - Use `shutil.copy2()` for file copying with metadata preservation
   - Apply filtering rules during traversal

4. **Progress Module** (`progress.py`)
   - Count total eligible files for accurate progress
   - Integrate `tqdm` for terminal-based progress bars
   - Support verbose mode output

5. **Installer Module** (`installer.py`)
   - Handle package installation and executable permissions
   - Cross-platform compatibility

## Development Standards

### Code Quality (following project conventions)
- **Python Version**: 3.13+ compatibility
- **Type Hints**: Strict typing with modern syntax (`list[str]` not `List[str]`)
- **Docstrings**: PEP 257 compliant with parameter and return documentation
- **Style**: PEP 8 compliance (4-space indentation, 79 character limit)
- **Error Handling**: Comprehensive exception handling with graceful degradation

### Dependencies Management
- **Runtime Dependencies**: Add `tqdm` for progress bars
- **Dev Dependencies**: Use existing `pytest>=8` and `ruff` setup
- **Package Management**: Use `uv` for all dependency operations

### Entry Point Configuration
- Update `pyproject.toml` to map CLI command to main function
- Current: `backup-py-projects = "backup_py_projects:hello"`
- Target: `backup-py-projects = "backup_py_projects:main"`

## Implementation Steps

### Phase 1: Core Infrastructure ✅ COMPLETED
1. ✅ Set up module structure in `src/backup_py_projects/`
2. ✅ Add `tqdm` dependency: `uv add tqdm`
3. ✅ Create argument parser with required CLI interface
4. ✅ Implement basic directory traversal and copying

**Phase 1 Accomplishments:**
- **Module Structure Created**: 
  - `cli.py` - Command-line argument parsing and path validation
  - `copier.py` - Core directory copying with `DirectoryCopier` class
  - `progress.py` - Progress tracking using `ProgressTracker` with tqdm integration
  - Updated `__init__.py` - Main entry point with `main()` function
- **Dependencies**: Added `tqdm>=4.67.1` for progress bars
- **CLI Interface**: Full `argparse` implementation with all required arguments:
  - Positional: source and destination directories
  - Optional: `--ignore-copy`, `--verbose`, `--install` flags
- **Entry Point**: Updated `pyproject.toml` to map `backup-py-projects` to `backup_py_projects:main`
- **Core Functionality**: 
  - Recursive directory copying using `os.walk()` and `shutil.copy2()`
  - Preserves directory structure and file metadata
  - Progress tracking with both verbose mode and tqdm progress bars
  - Comprehensive error handling with graceful degradation
- **Code Quality**: PEP 8 compliant, passes `ruff` linting, strict typing with modern syntax
- **Testing**: Successfully tested with file copying scenarios - confirmed working on Windows

### Phase 2: Filtering System ✅ COMPLETED
1. ✅ Create `filters.py` module for `.ignorecopy` file parsing
2. ✅ Implement glob pattern matching with `fnmatch`
3. ✅ Add gitignore-style pattern syntax support
4. ✅ Integrate filtering with directory traversal in `copier.py`
5. ✅ Add `--ignore-copy` override functionality
6. ✅ Add unit tests for filtering logic

**Phase 2 Accomplishments:**
- **Complete Filtering System**: Created `filters.py` with `IgnoreCopyFilter` and `FilterManager` classes
- **Pattern Matching**: Implemented glob pattern matching using `fnmatch` for gitignore-style patterns
- **Hierarchical Support**: `.ignorecopy` files are loaded from directory hierarchy (child overrides parent)
- **Directory Filtering**: Directories can be excluded with patterns ending in `/`
- **File Filtering**: Files are filtered by name, path, and parent directory patterns
- **Override Functionality**: `--ignore-copy` flag completely bypasses filtering
- **Caching**: Filter patterns are cached for performance
- **Error Handling**: Graceful handling of malformed `.ignorecopy` files and encoding issues
- **Cross-Platform**: Path separators normalized for Windows/Linux compatibility

**Testing Verified:**
- ✅ Basic pattern matching (`*.log`, `*.tmp`, `secret.txt`)
- ✅ Directory exclusion (`__pycache__/`, `.git/`, `node_modules/`)
- ✅ Hierarchical filtering (nested `.ignorecopy` files override parent)
- ✅ Override functionality (`--ignore-copy` copies everything)
- ✅ File counting respects filters
- ✅ Progress tracking works with filtered operations
- ✅ Code passes `ruff` linting and formatting checks

### Phase 3: User Experience 📋 PLANNED
1. ✅ Integrate `tqdm` progress bars (Already completed in Phase 1)
2. ✅ Implement verbose mode output (Already completed in Phase 1) 
3. ✅ Add comprehensive error handling (Already completed in Phase 1)
4. Cross-platform testing (Windows/Linux) - partially tested
5. Performance optimization for large directory structures

### Phase 4: Installation & Packaging 📋 PLANNED
1. Implement `--install` functionality (placeholder currently exists)
2. Update `pyproject.toml` entry points ✅ (Already completed in Phase 1)
3. Test package installation and CLI availability ✅ (Already completed in Phase 1)
4. Documentation and usage examples

## Testing Strategy

### Unit Tests (using pytest)
- Test each module independently
- Mock file system operations for reliable testing
- Test edge cases (empty directories, permission errors, invalid patterns)
- Cross-platform compatibility tests

### Integration Tests
- End-to-end copying scenarios
- `.ignorecopy` pattern matching validation
- Progress bar functionality
- CLI argument processing

## Current Status

**Phase 1: ✅ COMPLETED**
- All core infrastructure is in place and tested
- CLI interface fully functional with all required arguments
- Basic directory copying working with progress tracking

**Phase 2: ✅ COMPLETED**
- Complete `.ignorecopy` filtering system implemented and tested
- Hierarchical pattern loading working correctly
- All filtering patterns and override functionality verified

**Next Steps: Phase 3 - User Experience Enhancements**
- Cross-platform testing (Windows/Linux)
- Performance optimization for large directory structures
- Enhanced error handling and reporting

**Testing Results:**
- ✅ CLI help output working correctly
- ✅ Directory copying with progress bars (both verbose and non-verbose modes)
- ✅ `.ignorecopy` filtering with glob patterns (`*.log`, `*.tmp`, `__pycache__/`)
- ✅ Hierarchical filtering (nested `.ignorecopy` files)
- ✅ Override functionality (`--ignore-copy` flag)
- ✅ Error handling and path validation
- ✅ Code passes `ruff` linting and formatting checks
- ✅ Cross-platform path handling (Windows tested)

## Success Criteria

1. **Functional**: Successfully copy directory structures with exclusions
2. **User-Friendly**: Clear progress indication and error messages  
3. **Robust**: Handle edge cases and errors gracefully
4. **Cross-Platform**: Work on both Windows and Linux
5. **Standards-Compliant**: Follow project conventions and Python best practices
6. **Installable**: Deploy as system-wide Python package

## Example Usage

```bash
# Basic usage
uv run backup-py-projects /source/path /destination/path

# With verbose output
uv run backup-py-projects /source/path /destination/path --verbose

# Override exclusions
uv run backup-py-projects /source/path /destination/path --ignore-copy

# Install system-wide
uv run backup-py-projects --install
```