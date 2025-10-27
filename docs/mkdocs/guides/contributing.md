# Contributing

Thank you for your interest in contributing to VFN-RAG!

## Development Setup

1. Fork the repository
2. Clone your fork:

```bash
git clone https://github.com/your-username/vfn-rag.git
cd vfn-rag
```

3. Install development dependencies:

```bash
poetry install
```

4. Set up pre-commit hooks:

```bash
poetry run pre-commit install
```

## Branch Naming

When creating branches, use the following prefixes:
- `feat/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `chore/` - Tasks, tool changes, configuration work

Example: `feat/add-new-retrieval-method`

## Pull Requests

1. Create a branch from `main`
2. Make your changes
3. Ensure tests pass: `poetry run pytest`
4. Create a pull request with a clear description
5. Link to related issues using keywords like `Fixes #123`

## Code Quality

- Use black for code formatting: `poetry run black .`
- Use isort for import sorting: `poetry run isort .`
- Run linting: `poetry run flake8`

## Testing

Write tests for new features:

```bash
poetry run pytest
```

## Documentation

- Update documentation for API changes
- Follow the Google docstring style
- Update relevant guides if needed

## Commit Messages

Use conventional commit messages:

```
feat: Add new RAG retrieval method
fix: Fix storage loading issue
docs: Update installation guide
```

## Questions?

Feel free to open an issue for questions or discussions.

