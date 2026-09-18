#!/usr/bin/env python3
"""
Secure password generator CLI tool.
Uses cryptographically secure randomness. Zero dependencies.
"""

import argparse
import secrets
import string
import sys


# Character sets
LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SPECIAL = '!@#$%^&*()_+-=[]{}|;:,.<>?'

# Ambiguous characters to optionally exclude
AMBIGUOUS = '0O1lI'


def build_charset(use_lowercase, use_uppercase, use_numbers, use_special, no_ambiguous):
    """Build character set based on user flags."""
    charset = ''

    if use_lowercase:
        charset += LOWERCASE
    if use_uppercase:
        charset += UPPERCASE
    if use_numbers:
        charset += DIGITS
    if use_special:
        charset += SPECIAL

    if not charset:
        return None

    if no_ambiguous:
        charset = ''.join(c for c in charset if c not in AMBIGUOUS)

    return charset


def generate_password(length, charset):
    """Generate a single password using cryptographically secure randomness."""
    if not charset:
        raise ValueError("Character set is empty")

    return ''.join(secrets.choice(charset) for _ in range(length))


def main():
    parser = argparse.ArgumentParser(
        description='Generate secure random passwords using cryptographically secure randomness.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s                          # Generate one 16-character password
  %(prog)s --length 32              # Generate 32-character password
  %(prog)s --count 5                # Generate 5 passwords
  %(prog)s --no-special             # Exclude special characters
  %(prog)s --no-ambiguous           # Exclude ambiguous characters (0, O, 1, l, I)
  %(prog)s --no-uppercase --no-special  # Only lowercase and numbers
        '''
    )

    parser.add_argument(
        '--length',
        type=int,
        default=16,
        metavar='N',
        help='Password length (default: 16, range: 8-128)'
    )

    parser.add_argument(
        '--count',
        type=int,
        default=1,
        metavar='N',
        help='Number of passwords to generate (default: 1)'
    )

    parser.add_argument(
        '--no-lowercase',
        action='store_true',
        help='Exclude lowercase letters (a-z)'
    )

    parser.add_argument(
        '--no-uppercase',
        action='store_true',
        help='Exclude uppercase letters (A-Z)'
    )

    parser.add_argument(
        '--no-numbers',
        action='store_true',
        help='Exclude numbers (0-9)'
    )

    parser.add_argument(
        '--no-special',
        action='store_true',
        help='Exclude special characters'
    )

    parser.add_argument(
        '--no-ambiguous',
        action='store_true',
        help='Exclude ambiguous characters (0, O, 1, l, I)'
    )

    args = parser.parse_args()

    # Validate length
    if args.length < 8 or args.length > 128:
        sys.stderr.write(f"Error: Length must be between 8 and 128 (got {args.length})\n")
        sys.exit(1)

    # Validate count
    if args.count < 1:
        sys.stderr.write(f"Error: Count must be at least 1 (got {args.count})\n")
        sys.exit(1)

    # Build character set
    use_lowercase = not args.no_lowercase
    use_uppercase = not args.no_uppercase
    use_numbers = not args.no_numbers
    use_special = not args.no_special

    # At least one character type must be enabled
    if not any([use_lowercase, use_uppercase, use_numbers, use_special]):
        sys.stderr.write("Error: At least one character type must be enabled\n")
        sys.exit(1)

    charset = build_charset(
        use_lowercase,
        use_uppercase,
        use_numbers,
        use_special,
        args.no_ambiguous
    )

    if not charset:
        sys.stderr.write("Error: Character set is empty after applying filters\n")
        sys.exit(1)

    # Generate passwords
    try:
        for _ in range(args.count):
            password = generate_password(args.length, charset)
            print(password)
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
