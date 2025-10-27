# Pre-Commit Hooks

Pre-commit hooks help maintain code quality and consistency in VFN-RAG.

## What are Pre-Commit Hooks?

Pre-commit hooks are scripts that run automatically before you commit code. They check for:
- Code formatting (black, isort)
- Linting (flake8)
- Test execution
- Commit message format

## Installation

1. Install pre-commit:

```bash
poetry run pre-commit install
```

## Usage

Hooks run automatically when you commit. To run manually:

```bash
poetry run pre-commit run --all-files
```

## Configured Hooks

### Code Formatting
- **black**: Automatic Python code formatting
- **isort**: Import statement sorting

### Linting
- **flake8**: Python linting

### Testing
- **pytest**: Run unit tests
- **nbval**: Validate Jupyter notebooks

### Git Checks
- Prevents commits to protected branches
- Validates commit messages

## Skipping Hooks

You can skip hooks (not recommended):

```bash
git commit --no-verify -m "message"
```

## Updating Hooks

To update hook versions:

```bash
poetry run pre-commit autoupdate
```

