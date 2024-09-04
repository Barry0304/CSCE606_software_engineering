import pytest
from src.main.utils import load_config, parse_args, is_valid_username
import json
import os

def test_load_config(monkeypatch, tmp_path):
    config_data = {
        "database": {
            "path": "test_db.sqlite"
        }
    }
    config_path = tmp_path / "config.json"
    with open(config_path, 'w') as f:
        json.dump(config_data, f)

    monkeypatch.setattr('builtins.open', lambda *args: open(config_path, *args))

    config = load_config()
    assert config["database"]["path"] == "test_db.sqlite"

def test_parse_args():

    args = 'username="john_doe" password="12345" name="John Doe"'
    parsed_args = parse_args(args)
    assert parsed_args["username"] == "john_doe"
    assert parsed_args["password"] == "12345"
    assert parsed_args["name"] == "John Doe"

    args = 'status="active user"'
    parsed_args = parse_args(args)
    assert parsed_args["status"] == "active user"

    args = 'username=john_doe password=12345'
    parsed_args = parse_args(args)
    assert parsed_args["username"] == "john_doe"
    assert parsed_args["password"] == "12345"

def test_is_valid_username():
    assert is_valid_username("valid_username123") is True
    assert is_valid_username("ValidUser_456") is True
    assert is_valid_username("invalid username") is False
    assert is_valid_username("invalid-user") is False
    assert is_valid_username("invalid@user") is False 