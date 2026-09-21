#!/usr/bin/env python3
"""
Password Generator CLI

Generates cryptographically strong random passwords with configurable options.
Test fixture for AgentKit lifecycle workflow engine.
"""

import argparse
import json
import secrets
import string
import sys
from typing import List


def build_character_pool(
    use_uppercase: bool,
    use_lowercase: bool,
    use_digits: bool,
    use_symbols: bool,
) -> str:
    """Build the character pool from enabled character sets."""
    pool = ""
    if use_uppercase:
        pool += string.ascii_uppercase
    if use_lowercase:
        pool += string.ascii_lowercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    return pool


def generate_password(length: int, character_pool: str) -> str:
    """Generate a single password of the specified length."""
    return "".join(secrets.choice(character_pool) for _ in range(length))


def generate_passwords(
    count: int,
    length: int,
    character_pool: str,
) -> List[str]:
    """Generate multiple passwords."""
    return [generate_password(length, character_pool) for _ in range(count)]


def format_output(passwords: List[str], output_format: str) -> str:
    """Format the passwords according to the requested output format."""
    if output_format == "json":
        return json.dumps({"passwords": passwords}, indent=2)
    else:  # text
        return "\n".join(passwords)


def main():
    parser = argparse.ArgumentParser(
        description="Generate cryptographically strong random passwords"
    )

    parser.add_argument(
        "--length",
        type=int,
        default=16,
        help="Password length (default: 16)",
    )

    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of passwords to generate (default: 1)",
    )

    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    parser.add_argument(
        "--no-uppercase",
        action="store_true",
        help="Exclude uppercase letters",
    )

    parser.add_argument(
        "--no-lowercase",
        action="store_true",
        help="Exclude lowercase letters",
    )

    parser.add_argument(
        "--no-digits",
        action="store_true",
        help="Exclude digits",
    )

    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Exclude symbols",
    )

    args = parser.parse_args()

    # Validate length
    if args.length < 1:
        print("Error: Password length must be at least 1", file=sys.stderr)
        sys.exit(1)

    if args.count < 1:
        print("Error: Count must be at least 1", file=sys.stderr)
        sys.exit(1)

    # Build character pool
    character_pool = build_character_pool(
        use_uppercase=not args.no_uppercase,
        use_lowercase=not args.no_lowercase,
        use_digits=not args.no_digits,
        use_symbols=not args.no_symbols,
    )

    # Validate that at least one character set is enabled
    if not character_pool:
        print(
            "Error: At least one character set must be enabled",
            file=sys.stderr,
        )
        sys.exit(1)

    # Generate passwords
    passwords = generate_passwords(args.count, args.length, character_pool)

    # Output
    print(format_output(passwords, args.format))


if __name__ == "__main__":
    main()
