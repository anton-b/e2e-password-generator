"""CLI integration tests."""

import json
import subprocess
import sys
import pytest


def run_cli(*args):
    """Run the CLI and return the result."""
    result = subprocess.run(
        [sys.executable, "passgen.py"] + list(args),
        capture_output=True,
        text=True,
    )
    return result


class TestCLIDefaults:
    def test_default_generates_one_password(self):
        result = run_cli()
        assert result.returncode == 0
        passwords = result.stdout.strip().split("\n")
        assert len(passwords) == 1

    def test_default_length_is_16(self):
        result = run_cli()
        assert result.returncode == 0
        password = result.stdout.strip()
        assert len(password) == 16

    def test_default_includes_all_character_sets(self):
        # Run multiple times to ensure all character sets appear with high probability
        all_output = ""
        for _ in range(10):
            result = run_cli("--length", "50")
            all_output += result.stdout

        # With 500 characters total, we should see all character types
        assert any(c.isupper() for c in all_output)
        assert any(c.islower() for c in all_output)
        assert any(c.isdigit() for c in all_output)
        assert any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in all_output)


class TestCLILength:
    def test_custom_length(self):
        for length in ["8", "12", "32"]:
            result = run_cli("--length", length)
            assert result.returncode == 0
            password = result.stdout.strip()
            assert len(password) == int(length)

    def test_length_validation(self):
        result = run_cli("--length", "0")
        assert result.returncode == 1
        assert "Password length must be at least 1" in result.stderr


class TestCLICount:
    def test_multiple_passwords(self):
        result = run_cli("--count", "5")
        assert result.returncode == 0
        passwords = result.stdout.strip().split("\n")
        assert len(passwords) == 5

    def test_count_validation(self):
        result = run_cli("--count", "0")
        assert result.returncode == 1
        assert "Count must be at least 1" in result.stderr


class TestCLIFormat:
    def test_text_format(self):
        result = run_cli("--count", "3", "--format", "text")
        assert result.returncode == 0
        passwords = result.stdout.strip().split("\n")
        assert len(passwords) == 3

    def test_json_format(self):
        result = run_cli("--count", "3", "--format", "json")
        assert result.returncode == 0
        parsed = json.loads(result.stdout)
        assert "passwords" in parsed
        assert len(parsed["passwords"]) == 3


class TestCLICharacterSets:
    def test_no_uppercase(self):
        result = run_cli("--no-uppercase", "--length", "50")
        assert result.returncode == 0
        password = result.stdout.strip()
        assert not any(c.isupper() for c in password)
        assert any(c.islower() for c in password)

    def test_no_lowercase(self):
        result = run_cli("--no-lowercase", "--length", "50")
        assert result.returncode == 0
        password = result.stdout.strip()
        assert not any(c.islower() for c in password)
        assert any(c.isupper() for c in password)

    def test_no_digits(self):
        result = run_cli("--no-digits", "--length", "50")
        assert result.returncode == 0
        password = result.stdout.strip()
        assert not any(c.isdigit() for c in password)

    def test_no_symbols(self):
        result = run_cli("--no-symbols", "--length", "50")
        assert result.returncode == 0
        password = result.stdout.strip()
        assert not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

    def test_only_digits(self):
        result = run_cli(
            "--no-uppercase",
            "--no-lowercase",
            "--no-symbols",
            "--length", "20"
        )
        assert result.returncode == 0
        password = result.stdout.strip()
        assert all(c.isdigit() for c in password)

    def test_all_disabled_fails(self):
        result = run_cli(
            "--no-uppercase",
            "--no-lowercase",
            "--no-digits",
            "--no-symbols",
        )
        assert result.returncode == 1
        assert "At least one character set must be enabled" in result.stderr


class TestCLIHelp:
    def test_help_flag(self):
        result = run_cli("--help")
        assert result.returncode == 0
        assert "Password length" in result.stdout
        assert "Number of passwords" in result.stdout
        assert "Output format" in result.stdout
