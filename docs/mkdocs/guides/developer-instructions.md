# Developer Instructions

Guidelines and instructions for developers working on VFN-RAG.

## Overview

This page contains developer-focused documentation for contributing to VFN-RAG.

## Important Links

- [Contributing Guide](contributing.md) - How to contribute to the project
- [Pre-Commit Hooks](pre-commit-hooks.md) - Setup and usage of pre-commit hooks
- [Testing Guide](testing.md) - Testing conventions and practices

## Development Workflow

1. Create a feature branch
2. Make your changes
3. Run tests: `poetry run pytest`
4. Format code: `poetry run black .`
5. Commit with conventional commit messages
6. Create a pull request

## Tools

### Poetry

We use Poetry for dependency management. See the [Poetry documentation](https://python-poetry.org/docs/) for details.

### Pytest

We use pytest for testing:

```bash
poetry run pytest
```

### Black

We use black for code formatting:

```bash
poetry run black .
```

### Pre-Commit Hooks

Pre-commit hooks automatically check code quality before commits. See the [Pre-Commit Hooks guide](pre-commit-hooks.md) for setup instructions.

