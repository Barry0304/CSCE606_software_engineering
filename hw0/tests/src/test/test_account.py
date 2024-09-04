import pytest
from ..main.account import Account

def test_account_creation():
    account = Account(username="testuser", password="password123", name="Test User", status="active")
    assert account.username == "testuser"
    assert account.password == "password123"
    assert account.name == "Test User"
    assert account.status == "active"
    assert account.updated is not None
    assert account.session_token is not None


def test_account_update_name():
    account = Account(username="testuser", password="password123", name="Test User", status="active")
    account.update_name("Updated User")
    assert account.name == "Updated User"

def test_account_update_status():
    account = Account(username="testuser", password="password123", name="Test User", status="active")
    account.update_status("inactive")
    assert account.status == "inactive"

def test_update_status_unchanged():
    account = Account(username="testuser", password="password123", name="Test User", status="active")
    original_updated_time = account.updated
    result = account.update_status("active")
    assert result is False 
    assert account.status == "active"
    assert account.updated == original_updated_time

def test_update_name_unchanged():
    account = Account(username="testuser", password="password123", name="Test User", status="active")
    original_updated_time = account.updated
    result = account.update_name("Test User")
    assert result is False 
    assert account.name == "Test User"
    assert account.updated == original_updated_time 

def test_account_logout():
    account = Account(username="testuser", password="password123", name="Test User", status="active")
    original_session_token = account.session_token
    assert original_session_token is not None
    account.logout()
    assert account.session_token is None 