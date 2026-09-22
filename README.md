# Password Generator CLI

**Test fixture for AgentKit lifecycle workflow engine.**

Generates cryptographically strong random passwords with configurable options.

## Disclaimer

This is a test fixture for exercising the AgentKit workflow engine end-to-end. It is not production software and comes with no promises of maintenance or support.

## Installation

```bash
pip install .
```

## Usage

Generate a single 16-character password (default):
```bash
passgen
```

Generate multiple passwords:
```bash
passgen --count 5
```

Specify password length:
```bash
passgen --length 32
```

Output as JSON:
```bash
passgen --count 3 --format json
```

Customize character sets:
```bash
# Only digits
passgen --no-uppercase --no-lowercase --no-symbols

# No symbols
passgen --no-symbols

# Only uppercase and digits
passgen --no-lowercase --no-symbols
```

## Options

- `--length N`: Password length (default: 16)
- `--count N`: Number of passwords to generate (default: 1)
- `--format {text,json}`: Output format (default: text)
- `--no-uppercase`: Exclude uppercase letters
- `--no-lowercase`: Exclude lowercase letters
- `--no-digits`: Exclude digits
- `--no-symbols`: Exclude symbols
- `-h, --help`: Show help message

All character sets are enabled by default.

## Development

Run tests:
```bash
pytest tests/ -v
```

## Requirements

Python 3.8+

## License

MIT
