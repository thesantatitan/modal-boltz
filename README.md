# Modal Boltz

A Python CLI tool built with Modal and Boltz.

## Installation

### From PyPI (once published)

```bash
pip install modal-boltz
```

### From source

```bash
# Clone the repository
git clone https://github.com/yourusername/modal-boltz.git
cd modal-boltz

# Install in development mode
pip install -e .
```

### Using uv (recommended for development)

```bash
# Install dependencies
uv sync

# Install in development mode
uv pip install -e .
```

## Usage

Once installed, you can use the `modal-boltz` command:

```bash
# Basic hello command
modal-boltz hello

# Hello with custom name
modal-boltz hello --name "Alice"

# Show version and info
modal-boltz info

# Show help
modal-boltz --help
```

## Development

This project uses `uv` for dependency management. To set up for development:

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Run the CLI in development
uv run python -m modal_boltz.cli --help
```

## Commands

- `hello` - Say hello (with optional --name parameter)
- `info` - Show version and project information
- `--version` - Show version number
- `--help` - Show help message

## License

MIT