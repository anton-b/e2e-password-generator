#!/usr/bin/env python3
"""
Tests for genpass.py password generator.
Run with: python3 test_genpass.py
"""

import subprocess
import sys
import re


def run_genpass(*args):
    """Run genpass.py and return (exit_code, stdout, stderr)."""
    cmd = [sys.executable, 'genpass.py'] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def test_default_generation():
    """Test default password generation (16 characters, all types)."""
    code, stdout, stderr = run_genpass()
    assert code == 0, f"Expected exit code 0, got {code}"
    assert stderr == '', f"Expected no stderr, got: {stderr}"

    lines = stdout.strip().split('\n')
    assert len(lines) == 1, f"Expected 1 password, got {len(lines)}"

    password = lines[0]
    assert len(password) == 16, f"Expected 16 characters, got {len(password)}"
    print("✓ Default generation works")


def test_length_flag():
    """Test --length flag."""
    code, stdout, stderr = run_genpass('--length', '32')
    assert code == 0, f"Expected exit code 0, got {code}"

    password = stdout.strip()
    assert len(password) == 32, f"Expected 32 characters, got {len(password)}"
    print("✓ --length flag works")


def test_count_flag():
    """Test --count flag."""
    code, stdout, stderr = run_genpass('--count', '5')
    assert code == 0, f"Expected exit code 0, got {code}"

    lines = stdout.strip().split('\n')
    assert len(lines) == 5, f"Expected 5 passwords, got {len(lines)}"

    # Check all passwords are 16 characters (default)
    for pwd in lines:
        assert len(pwd) == 16, f"Expected 16 characters, got {len(pwd)}"

    print("✓ --count flag works")


def test_no_uppercase():
    """Test --no-uppercase excludes uppercase letters."""
    code, stdout, stderr = run_genpass('--no-uppercase', '--length', '50')
    assert code == 0, f"Expected exit code 0, got {code}"

    password = stdout.strip()
    assert not any(c.isupper() for c in password), "Password contains uppercase letters"
    print("✓ --no-uppercase works")


def test_no_lowercase():
    """Test --no-lowercase excludes lowercase letters."""
    code, stdout, stderr = run_genpass('--no-lowercase', '--length', '50')
    assert code == 0, f"Expected exit code 0, got {code}"

    password = stdout.strip()
    assert not any(c.islower() for c in password), "Password contains lowercase letters"
    print("✓ --no-lowercase works")


def test_no_numbers():
    """Test --no-numbers excludes digits."""
    code, stdout, stderr = run_genpass('--no-numbers', '--length', '50')
    assert code == 0, f"Expected exit code 0, got {code}"

    password = stdout.strip()
    assert not any(c.isdigit() for c in password), "Password contains digits"
    print("✓ --no-numbers works")


def test_no_special():
    """Test --no-special excludes special characters."""
    code, stdout, stderr = run_genpass('--no-special', '--length', '50')
    assert code == 0, f"Expected exit code 0, got {code}"

    password = stdout.strip()
    # Should only contain alphanumeric
    assert password.isalnum(), "Password contains special characters"
    print("✓ --no-special works")


def test_no_ambiguous():
    """Test --no-ambiguous excludes ambiguous characters."""
    # Generate many passwords to increase likelihood of encountering ambiguous chars if bug exists
    code, stdout, stderr = run_genpass('--no-ambiguous', '--count', '20', '--length', '50')
    assert code == 0, f"Expected exit code 0, got {code}"

    ambiguous = '0O1lI'
    passwords = stdout.strip().split('\n')

    for password in passwords:
        for char in ambiguous:
            assert char not in password, f"Password contains ambiguous character '{char}'"

    print("✓ --no-ambiguous works")


def test_invalid_length_low():
    """Test length below minimum (8) fails."""
    code, stdout, stderr = run_genpass('--length', '7')
    assert code != 0, f"Expected non-zero exit code, got {code}"
    assert 'Error' in stderr, "Expected error message in stderr"
    print("✓ Length validation (too low) works")


def test_invalid_length_high():
    """Test length above maximum (128) fails."""
    code, stdout, stderr = run_genpass('--length', '129')
    assert code != 0, f"Expected non-zero exit code, got {code}"
    assert 'Error' in stderr, "Expected error message in stderr"
    print("✓ Length validation (too high) works")


def test_all_types_excluded():
    """Test that excluding all character types fails."""
    code, stdout, stderr = run_genpass(
        '--no-lowercase',
        '--no-uppercase',
        '--no-numbers',
        '--no-special'
    )
    assert code != 0, f"Expected non-zero exit code, got {code}"
    assert 'Error' in stderr, "Expected error message in stderr"
    assert 'character type' in stderr.lower(), "Error should mention character types"
    print("✓ All types excluded validation works")


def test_help():
    """Test --help flag."""
    code, stdout, stderr = run_genpass('--help')
    assert code == 0, f"Expected exit code 0, got {code}"
    assert 'usage:' in stdout.lower() or 'usage:' in stderr.lower(), "Expected usage text"
    assert '--length' in stdout or '--length' in stderr, "Expected --length flag in help"
    assert '--count' in stdout or '--count' in stderr, "Expected --count flag in help"
    print("✓ --help works")


def test_randomness():
    """Test that passwords are different (basic randomness check)."""
    code, stdout, stderr = run_genpass('--count', '10')
    assert code == 0, f"Expected exit code 0, got {code}"

    passwords = stdout.strip().split('\n')
    unique_passwords = set(passwords)

    assert len(unique_passwords) == 10, "Passwords are not unique (randomness issue)"
    print("✓ Randomness check passed (10 unique passwords)")


def test_min_length():
    """Test minimum valid length (8)."""
    code, stdout, stderr = run_genpass('--length', '8')
    assert code == 0, f"Expected exit code 0, got {code}"

    password = stdout.strip()
    assert len(password) == 8, f"Expected 8 characters, got {len(password)}"
    print("✓ Minimum length (8) works")


def test_max_length():
    """Test maximum valid length (128)."""
    code, stdout, stderr = run_genpass('--length', '128')
    assert code == 0, f"Expected exit code 0, got {code}"

    password = stdout.strip()
    assert len(password) == 128, f"Expected 128 characters, got {len(password)}"
    print("✓ Maximum length (128) works")


def test_combined_flags():
    """Test combining multiple flags."""
    code, stdout, stderr = run_genpass(
        '--length', '24',
        '--count', '3',
        '--no-special',
        '--no-ambiguous'
    )
    assert code == 0, f"Expected exit code 0, got {code}"

    passwords = stdout.strip().split('\n')
    assert len(passwords) == 3, f"Expected 3 passwords, got {len(passwords)}"

    ambiguous = '0O1lI'
    for password in passwords:
        assert len(password) == 24, f"Expected 24 characters, got {len(password)}"
        assert password.isalnum(), "Password should be alphanumeric only"
        for char in ambiguous:
            assert char not in password, f"Password contains ambiguous character '{char}'"

    print("✓ Combined flags work")


def main():
    """Run all tests."""
    print("Running genpass.py tests...\n")

    tests = [
        test_default_generation,
        test_length_flag,
        test_count_flag,
        test_no_uppercase,
        test_no_lowercase,
        test_no_numbers,
        test_no_special,
        test_no_ambiguous,
        test_invalid_length_low,
        test_invalid_length_high,
        test_all_types_excluded,
        test_help,
        test_randomness,
        test_min_length,
        test_max_length,
        test_combined_flags,
    ]

    failed = []

    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed.append(test.__name__)
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed.append(test.__name__)

    print(f"\n{'='*60}")
    print(f"Tests run: {len(tests)}")
    print(f"Passed: {len(tests) - len(failed)}")
    print(f"Failed: {len(failed)}")

    if failed:
        print(f"\nFailed tests: {', '.join(failed)}")
        sys.exit(1)
    else:
        print("\nAll tests passed! ✓")
        sys.exit(0)


if __name__ == '__main__':
    main()
