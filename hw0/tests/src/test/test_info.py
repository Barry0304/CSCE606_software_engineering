import pytest
from src.main.info import (
    show_info, 
    show_person, 
    show_people, 
    show_info_with_session_token, 
    show_session_token_invalid, 
    show_info_with_account, 
    show_people_with_session_token,
    show_person_with_session_token,
    find_account,
    find_account_with_session_token,
    sort_account
)
from src.main.db import insert_account_to_db, db_reset
from src.main.account import Account


@pytest.fixture(autouse=True)

def test_show_info(capsys):
    show_info()
    captured = capsys.readouterr()
    assert "Welcome to the App!" in captured.out

def test_show_person_existing_user(capsys):
    db_reset()
    account = Account(username="testuser", password="password123", name="Test User", status="active")
    insert_account_to_db(account)
    show_person("testuser")
    captured = capsys.readouterr()
    assert "Person" in captured.out
    assert "testuser" in captured.out
    db_reset()

def test_show_person_existing_user_one_at_a_time(capsys):
    db_reset()
    account = Account(username="testuser", password="password123", name="Test User", status="active")
    insert_account_to_db(account)
    show_person("testuser people")
    captured = capsys.readouterr()
    assert "Person" in captured.out
    assert "testuser" in captured.out
    db_reset()

def test_show_person_missing_username(capsys):
    db_reset()
    show_person("")
    captured = capsys.readouterr()
    assert "missing username" in captured.out

def test_show_person_non_existing_user(capsys):
    db_reset()
    show_person("nonexistent")
    captured = capsys.readouterr()
    assert "not found" in captured.out

def test_show_people_no_users(capsys):
    db_reset()
    show_people()
    captured = capsys.readouterr()
    assert "No one is here..." in captured.out

def test_show_people_with_users(capsys):
    db_reset()
    account1 = Account(username="user1", password="password1", name="User One", status="active")
    account2 = Account(username="user2", password="password2", name="User Two", status="busy")
    insert_account_to_db(account1)
    insert_account_to_db(account2)
    show_people()
    captured = capsys.readouterr()
    assert "User One" in captured.out
    assert "User Two" in captured.out
    db_reset()

def test_show_info_with_session_token_valid(capsys):
    db_reset()
    account = Account(username="testuser", password="password123", name="Test User", status="active", session_token="validtoken")
    insert_account_to_db(account)
    show_info_with_session_token("validtoken")
    captured = capsys.readouterr()
    assert "Welcome back to the App" in captured.out
    assert "edit" in captured.out
    db_reset()

def test_show_info_with_session_token_invalid(capsys):
    db_reset()
    show_info_with_session_token("invalidtoken")
    captured = capsys.readouterr()
    assert "invalid request: invalid session token" in captured.out

def test_show_info_with_account(capsys):
    db_reset()
    account = Account(username="testuser", password="password123", name="Test User", status="active", session_token="validtoken")
    insert_account_to_db(account)
    show_info_with_account(account)
    captured = capsys.readouterr()
    assert "Person" in captured.out
    assert "Test User" in captured.out
    db_reset()

def test_show_people_with_session_token_valid(capsys):
    db_reset()
    account = Account(username="testuser", password="password123", name="Test User", status="active", session_token="validtoken")
    insert_account_to_db(account)
    show_people_with_session_token("validtoken")
    captured = capsys.readouterr()
    assert "People" in captured.out
    assert "Test User" in captured.out
    db_reset()

def test_show_people_with_session_token_invalid(capsys):
    db_reset()
    account = Account(username="testuser", password="password123", name="Test User", status="active", session_token="validtoken")
    insert_account_to_db(account)
    show_people_with_session_token("invalidtoken")
    captured = capsys.readouterr()
    assert "invalid request: invalid session token" in captured.out

def test_show_person_with_session_token_valid(capsys):
    db_reset()
    account = Account(username="testuser", password="password123", name="Test User", status="active", session_token="validtoken")
    insert_account_to_db(account)
    show_person_with_session_token("validtoken", "testuser")
    captured = capsys.readouterr()
    assert "Person" in captured.out
    assert "Test User" in captured.out
    db_reset()

def test_show_person_with_session_token_invalid_token(capsys):
    db_reset()
    show_person_with_session_token("invalidtoken", "testuser")
    captured = capsys.readouterr()
    assert "invalid request: invalid session token" in captured.out

def test_show_person_with_session_token_missing_username(capsys):
    db_reset()
    show_person_with_session_token("invalidtoken", "")
    captured = capsys.readouterr()
    assert "invalid request: missing username" in captured.out

def test_show_person_with_session_token_invalid_username(capsys):
    db_reset()
    account = Account(username="testuser", password="password123", name="Test User", status="active", session_token="validtoken")
    insert_account_to_db(account)
    show_person_with_session_token("validtoken", "nonexistent")
    captured = capsys.readouterr()
    assert "not found" in captured.out
    db_reset()

def test_find_account_valid_pattern(capsys):
    db_reset()
    account1 = Account(username="user1", password="password1", name="User One", status="active")
    account2 = Account(username="user2", password="password2", name="User Two", status="busy")
    insert_account_to_db(account1)
    insert_account_to_db(account2)
    find_account("User")
    captured = capsys.readouterr()
    assert "User One" in captured.out
    assert "User Two" in captured.out
    db_reset()

def test_find_account_invalid_pattern(capsys):
    db_reset()
    find_account("nonexistent")
    captured = capsys.readouterr()
    assert "No one is here..." in captured.out

def test_find_account_valid_pattern_with_colon(capsys):
    db_reset()
    account1 = Account(username="user1", password="password1", name="User One", status="active")
    account2 = Account(username="user2", password="password2", name="User Two", status="busy")
    insert_account_to_db(account1)
    insert_account_to_db(account2)

    find_account("status:active")
    captured = capsys.readouterr()
    assert "User One" in captured.out
    assert "User Two" not in captured.out

    find_account("status:nonexistent")
    captured = capsys.readouterr()
    assert "No one is here..." in captured.out 
    db_reset()

def test_find_account_with_any_field(capsys):
    db_reset()
    account1 = Account(username="user1", password="password1", name="User One", status="active")
    account2 = Account(username="user2", password="password2", name="User Two", status="busy")
    insert_account_to_db(account1)
    insert_account_to_db(account2)

    find_account("busy")
    captured = capsys.readouterr()
    assert "User Two" in captured.out
    assert "User One" not in captured.out

    find_account("")
    captured = capsys.readouterr()
    assert "People (find all)" in captured.out
    assert "User Two" in captured.out
    assert "User One" in captured.out
    db_reset()


def test_find_account_with_session_token_valid(capsys):
    db_reset()
    account = Account(username="testuser", password="password123", name="Test User", status="active", session_token="validtoken")
    insert_account_to_db(account)
    find_account_with_session_token("validtoken")
    captured = capsys.readouterr()
    assert "People (find all)" in captured.out
    db_reset()

def test_find_account_with_session_token_invalid(capsys):
    db_reset()
    find_account_with_session_token("invalidtoken")
    captured = capsys.readouterr()
    assert "invalid request: invalid session token" in captured.out


def test_sort_account_default(capsys):
    db_reset()
    account1 = Account(username="user1", password="password1", name="User One", status="active", updated="2023-01-01")
    account2 = Account(username="user2", password="password2", name="User Two", status="busy", updated="2024-01-01")
    insert_account_to_db(account1)
    insert_account_to_db(account2)
    sort_account("")
    captured = capsys.readouterr()
    assert "User Two" in captured.out  
    assert "User One" in captured.out
    db_reset()

def test_sort_account_without_order(capsys):
    db_reset()
    account1 = Account(username="user1", password="password1", name="User One", status="active", updated="2024-01-01")
    account2 = Account(username="user2", password="password2", name="User Two", status="busy", updated="2023-01-01")
    insert_account_to_db(account1)
    insert_account_to_db(account2)
    sort_account("updated")
    captured = capsys.readouterr()
    assert "User Two" in captured.out  
    assert "User One" in captured.out
    db_reset()

def test_sort_account_without_order(capsys):
    db_reset()
    account1 = Account(username="user1", password="password1", name="User One", status="active", updated="2024-01-01")
    account2 = Account(username="user2", password="password2", name="User Two", status="busy", updated="2023-01-01")
    insert_account_to_db(account1)
    insert_account_to_db(account2)
    sort_account("status")
    captured = capsys.readouterr()
    assert "User Two" in captured.out  
    assert "User One" in captured.out
    db_reset()

def test_sort_account_asc(capsys):
    db_reset()
    account1 = Account(username="user1", password="password1", name="User One", status="active", updated="2024-01-01")
    account2 = Account(username="user2", password="password2", name="User Two", status="busy", updated="2023-01-01")
    insert_account_to_db(account1)
    insert_account_to_db(account2)
    sort_account("updated asc")
    captured = capsys.readouterr()
    assert "User Two" in captured.out  # Sorted by updated, asc
    assert "User One" in captured.out
    db_reset()

def test_sort_account_invalid_field(capsys):
    sort_account("invalidfield asc")
    captured = capsys.readouterr()
    assert "not found" in captured.out


def test_sort_account_invalid_order(capsys):
    sort_account("username invalidorder")
    captured = capsys.readouterr()
    assert "not found" in captured.out