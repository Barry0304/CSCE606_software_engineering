import pytest
from src.main.update import update_account, edit
from src.main.db import insert_account_to_db, get_account_by_session_token, db_reset
from src.main.account import Account


def test_update_account_valid(capsys):
    db_reset()
    account = Account(username="testuser", password="password123", name="Test User", status="active")
    insert_account_to_db(account)
    update_account(account.session_token, 'name="New Name" status="New Status"')
    captured = capsys.readouterr()
    assert "name and status updated" in captured.out
    updated_account = get_account_by_session_token(account.session_token)
    assert updated_account.name == "New Name"
    assert updated_account.status == "New Status"
    db_reset()

def test_update_account_name(capsys):
    db_reset()
    account = Account(username="testuser", password="password123", name="Test User", status="active")
    insert_account_to_db(account)
    update_account(account.session_token, 'name="New Name"')
    captured = capsys.readouterr()
    assert "name updated" in captured.out
    updated_account = get_account_by_session_token(account.session_token)
    assert updated_account.name == "New Name"
    assert updated_account.status == "active"
    db_reset()

def test_update_account_status(capsys):
    db_reset()
    account = Account(username="testuser", password="password123", name="Test User", status="active")
    insert_account_to_db(account)
    update_account(account.session_token,  'status="New Status"')
    captured = capsys.readouterr()
    assert "status updated" in captured.out
    updated_account = get_account_by_session_token(account.session_token)
    assert updated_account.name == "Test User"
    assert updated_account.status == "New Status"
    db_reset()

def test_update_account_name_too_short(capsys):
    db_reset()
    account = Account(username="testuser", password="password123", name="Test User", status="active")
    insert_account_to_db(account)
    update_account(account.session_token, 'name="ab" status="New Status"')
    updated_account = get_account_by_session_token(account.session_token)
    captured = capsys.readouterr()
    assert "failed to update: name is too short" in captured.out
    assert updated_account.name == "Test User"
    assert updated_account.status == "New Status"
    db_reset()

def test_update_account_name_too_long(capsys):
    db_reset()
    account = Account(username="testuser", password="password123", name="Test User", status="active")
    insert_account_to_db(account)
    update_account(account.session_token, 'name="aaaaaaaaaaaaaaaaaaaaa" status="New Status"')
    updated_account = get_account_by_session_token(account.session_token)
    captured = capsys.readouterr()
    assert "failed to update: name is too long" in captured.out
    assert updated_account.name == "Test User"
    assert updated_account.status == "New Status"
    db_reset()

def test_update_account_status_too_short(capsys):
    db_reset()
    account = Account(username="testuser", password="password123", name="Test User", status="active")
    insert_account_to_db(account)
    short_status = ""
    update_account(account.session_token, f'name="New Name" status="{short_status}"')
    updated_account = get_account_by_session_token(account.session_token)
    captured = capsys.readouterr()
    assert "failed to update: status is too short" in captured.out
    assert updated_account.name == "New Name"
    assert updated_account.status == "active"
    db_reset()

def test_update_account_status_too_long(capsys):
    db_reset()
    account = Account(username="testuser", password="password123", name="Test User", status="active")
    insert_account_to_db(account)
    long_status = "a" * 101
    update_account(account.session_token, f'name="New Name" status="{long_status}"')
    updated_account = get_account_by_session_token(account.session_token)
    captured = capsys.readouterr()
    assert "failed to update: status is too long" in captured.out
    assert updated_account.name == "New Name"
    assert updated_account.status == "active"
    db_reset()


def test_update_account_missing_name_and_status(capsys):
    db_reset()
    account = Account(username="testuser", password="password123", name="Test User", status="active")
    insert_account_to_db(account)
    update_account(account.session_token, '')
    updated_account = get_account_by_session_token(account.session_token)
    captured = capsys.readouterr()
    assert "failed to update: missing name and status" in captured.out
    assert updated_account.name == "Test User"
    assert updated_account.status == "active"
    db_reset()


def test_update_account_invalid_session_token(capsys):
    db_reset()
    update_account("invalid_token", 'name="New Name" status="New Status"')
    captured = capsys.readouterr()
    assert "invalid request: invalid session token" in captured.out
    assert "home: ./app" in captured.out
    db_reset()

def test_edit_function_valid(monkeypatch):
    db_reset()
    account = Account(username="edituser", password="password123", name="Edit User", status="active")
    insert_account_to_db(account)

    inputs = iter(['Edited Name', 'Edited Status'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    edit(account.session_token)
    updated_account = get_account_by_session_token(account.session_token)
    assert updated_account.name == "Edited Name"
    assert updated_account.status == "Edited Status"
    db_reset()

def test_edit_function_no_changes(monkeypatch):
    db_reset()
    account = Account(username="edituser", password="password123", name="Edit User", status="active")
    insert_account_to_db(account)

    inputs = iter(['', ''])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    edit(account.session_token)
    updated_account = get_account_by_session_token(account.session_token)
    assert updated_account.name == "Edit User"
    assert updated_account.status == "active"
    db_reset()

def test_edit_function_update_name_only(monkeypatch):
    db_reset()
    account = Account(username="edituser", password="password123", name="Edit User", status="active")
    insert_account_to_db(account)

    inputs = iter(['New Name', ''])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    edit(account.session_token)
    updated_account = get_account_by_session_token(account.session_token)
    assert updated_account.name == "New Name"
    assert updated_account.status == "active"
    db_reset()

def test_edit_function_update_status_only(monkeypatch):
    db_reset()
    account = Account(username="edituser", password="password123", name="Edit User", status="active")
    insert_account_to_db(account)

    inputs = iter(['', 'New Status'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    edit(account.session_token)
    updated_account = get_account_by_session_token(account.session_token)
    assert updated_account.name == "Edit User"  # Name should remain unchanged
    assert updated_account.status == "New Status"
    db_reset()

def test_edit_function_invalid_session_token(monkeypatch, capsys):
    db_reset()
    inputs = iter(['New Name', 'New Status'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    edit("invalid_token")
    
    captured = capsys.readouterr()
    assert "invalid request: invalid session token" in captured.out
    assert "home: ./app" in captured.out
    db_reset()