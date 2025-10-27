# CLI Module

The Command Line Interface (CLI) module provides command-line tools for interacting with VFN-RAG.

## Overview

VFN-RAG includes a CLI tool named `vfn-rag` that allows you to interact with the system via command-line commands.

## Installation

After installing the package, the CLI is available as:

```bash
poetry run vfn-rag
```

## Available Commands

### Hello Command

Test the CLI installation:

```bash
poetry run vfn-rag hello
```

Or with a custom name:

```bash
poetry run vfn-rag hello --name "Alice"
```

### Query Command

Process a RAG query:

```bash
poetry run vfn-rag query --query "What species live in Dutch ponds?" --max-results 10
```

**Parameters:**
- `--query` (required): The question to ask
- `--max-results` (optional, default=5): Maximum number of results to return

### Version Command

Show version information:

```bash
poetry run vfn-rag version
```

## API Reference

::: vfn_rag.cli

## Usage Examples

```bash
# Test the CLI
poetry run vfn-rag hello

# Ask a question
poetry run vfn-rag query --query "How does RAG work?" --max-results 5

# Check version
poetry run vfn-rag version
```

