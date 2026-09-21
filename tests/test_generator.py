"""Unit tests for password generation logic."""

import json
import string
import pytest
import sys
import os

# Add parent directory to path to import passgen
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import passgen


class TestCharacterPool:
    def test_all_character_sets_enabled(self):
        pool = passgen.build_character_pool(True, True, True, True)
        assert string.ascii_uppercase[0] in pool
        assert string.ascii_lowercase[0] in pool
        assert string.digits[0] in pool
        assert "!" in pool

    def test_only_uppercase(self):
        pool = passgen.build_character_pool(True, False, False, False)
        assert all(c in string.ascii_uppercase for c in pool)
        assert len(pool) == 26

    def test_only_lowercase(self):
        pool = passgen.build_character_pool(False, True, False, False)
        assert all(c in string.ascii_lowercase for c in pool)
        assert len(pool) == 26

    def test_only_digits(self):
        pool = passgen.build_character_pool(False, False, True, False)
        assert all(c in string.digits for c in pool)
        assert len(pool) == 10

    def test_only_symbols(self):
        pool = passgen.build_character_pool(False, False, False, True)
        assert all(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in pool)

    def test_empty_pool(self):
        pool = passgen.build_character_pool(False, False, False, False)
        assert pool == ""

    def test_multiple_character_sets(self):
        pool = passgen.build_character_pool(True, True, False, False)
        assert "A" in pool
        assert "a" in pool
        assert "0" not in pool


class TestPasswordGeneration:
    def test_password_length(self):
        pool = string.ascii_letters
        password = passgen.generate_password(16, pool)
        assert len(password) == 16

    def test_custom_length(self):
        pool = string.ascii_letters
        for length in [8, 12, 20, 32]:
            password = passgen.generate_password(length, pool)
            assert len(password) == length

    def test_uses_character_pool(self):
        pool = "ABC"
        password = passgen.generate_password(100, pool)
        assert all(c in pool for c in password)

    def test_multiple_passwords(self):
        pool = string.ascii_letters
        passwords = passgen.generate_passwords(5, 16, pool)
        assert len(passwords) == 5
        assert all(len(p) == 16 for p in passwords)

    def test_passwords_are_different(self):
        # With high probability, multiple passwords should be unique
        pool = string.ascii_letters + string.digits
        passwords = passgen.generate_passwords(100, 16, pool)
        unique_passwords = set(passwords)
        # Expect most passwords to be unique (allowing for tiny collision probability)
        assert len(unique_passwords) > 95


class TestOutputFormatting:
    def test_text_format_single(self):
        passwords = ["password1"]
        output = passgen.format_output(passwords, "text")
        assert output == "password1"

    def test_text_format_multiple(self):
        passwords = ["password1", "password2", "password3"]
        output = passgen.format_output(passwords, "text")
        assert output == "password1\npassword2\npassword3"

    def test_json_format_single(self):
        passwords = ["password1"]
        output = passgen.format_output(passwords, "json")
        parsed = json.loads(output)
        assert parsed == {"passwords": ["password1"]}

    def test_json_format_multiple(self):
        passwords = ["password1", "password2"]
        output = passgen.format_output(passwords, "json")
        parsed = json.loads(output)
        assert parsed == {"passwords": ["password1", "password2"]}
