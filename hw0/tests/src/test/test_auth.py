import pytest
from src.main.auth import vali_and_creat_account, login_account, create_account, delete_account, join_account, logout_account
from src.main.db import get_account_by_username, db_reset, session_token_in_db
from src.main.account import Account

@pytest.fixture(autouse=True)

def test_vali_and_create_account_valid():
    db_reset()
    vali_and_creat_account('newuser', 'password123', 'New User', 'active')
    account = get_account_by_username('newuser')
    assert account is not False
    assert account.username == 'newuser'
    db_reset()

def test_vali_and_create_account_existing_user():
    db_reset()
    vali_and_creat_account('existinguser', 'password123', 'Existing User', 'active')
    vali_and_creat_account('existinguser', 'newpassword', 'New Name', 'newstatus')
    account = get_account_by_username('existinguser')
    assert account is not False
    assert account.username == 'existinguser'
    assert account.name == 'Existing User'

def test_vali_and_create_account_invalid_username():
    db_reset()
    vali_and_creat_account('us__--++', 'password123', 'Invalid User', 'active')
    account = get_account_by_username('us__--++')
    assert account is False
    db_reset()

def test_vali_and_create_account_invalid_short_username():
    db_reset()
    vali_and_creat_account('us', 'password123', 'Invalid User', 'active')
    account = get_account_by_username('us')
    assert account is False
    db_reset()

def test_vali_and_create_account_invalid_long_username():
    db_reset()
    vali_and_creat_account('aaaaaaaaaaaaaaaaaaaaa', 'password123', 'Invalid User', 'active')
    account = get_account_by_username('aaaaaaaaaaaaaaaaaaaaa')
    assert account is False
    db_reset()

def test_vali_and_create_account_invalid_long_name():
    db_reset()
    vali_and_creat_account('newuser', 'password123', 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'active')
    account = get_account_by_username('newuser')
    assert account is False
    db_reset()

def test_vali_and_create_account_invalid_short_name():
    db_reset()
    vali_and_creat_account('newuser', 'password123', '', 'active')
    account = get_account_by_username('newuser')
    assert account is False
    db_reset()

def test_vali_and_create_account_invalid_short_status():
    db_reset()
    vali_and_creat_account('newuser', 'password123', 'Invalid User', '')
    account = get_account_by_username('newuser')
    assert account is False
    db_reset()

def test_vali_and_create_account_invalid_long_status():
    db_reset()
    vali_and_creat_account('newuser', 'password123', 'Invalid User', 'a'*101)
    account = get_account_by_username('newuser')
    assert account is False
    db_reset()

def test_vali_and_create_account_invalid_short_password():
    db_reset()
    vali_and_creat_account('newuser', 'pas', 'Invalid User', 'active')
    account = get_account_by_username('newuser')
    assert account is False
    db_reset()

def test_vali_and_create_account_invalid_password():
    db_reset()
    vali_and_creat_account('newuser', '"', 'Invalid User', 'active')
    account = get_account_by_username('newuser')
    assert account is False
    db_reset()

def test_vali_and_create_account_invalid_status():
    db_reset()
    vali_and_creat_account('newuser', 'pas', 'Invalid User', 'ati"ve')
    account = get_account_by_username('newuser')
    assert account is False
    db_reset()

def test_vali_and_create_account_invalid_name():
    db_reset()
    vali_and_creat_account('newuser', 'pas', 'Invalid"User', 'active')
    account = get_account_by_username('newuser')
    assert account is False
    db_reset()


def test_vali_and_create_account_invalid_name_with_double_quote():
    db_reset()
    vali_and_creat_account('newuser', 'pas', 'Invalid"User', 'active')
    account = get_account_by_username('newuser')
    assert account is False
    db_reset()

def test_vali_and_create_account_invalid_password_with_double_quote():
    db_reset()
    vali_and_creat_account('newuser', 'p"a"s', 'Invalid"User', 'active')
    account = get_account_by_username('newuser')
    assert account is False
    db_reset()

def test_vali_and_create_account_invalid_status_with_double_quote():
    db_reset()
    vali_and_creat_account('newus"er', 'pas', 'Invalid"User', 'ac"t"ive')
    account = get_account_by_username('newuser')
    assert account is False
    db_reset()

def test_login_account_no_args(capsys):
    login_account("")
    captured = capsys.readouterr()
    assert "invalid request: missing username and password" in captured.out
    assert "home: ./app" in captured.out

def test_login_account_only_username(capsys):
    login_account("loginuser")
    captured = capsys.readouterr()
    assert "access denied: incorrect username or password" in captured.out
    assert "home: ./app" in captured.out

def test_login_account_valid(capsys):
    db_reset()
    vali_and_creat_account('loginuser', 'password123', 'Login User', 'active')
    login_account('loginuser password123')
    captured = capsys.readouterr()
    assert "Welcome back to the App" in captured.out
    db_reset()

def test_login_account_invalid():
    assert login_account('unknownuser wrongpassword') is False

def test_create_account_valid():
    db_reset()
    create_account('username="test" password="password123" name="test" status="test"')
    account = get_account_by_username('test')
    assert account is not False
    assert account.username == 'test'
    assert account.name == 'test'
    db_reset()

def test_create_account_missing_username():
    db_reset()
    assert create_account('password="password123" name="test" status="test"') is False
    db_reset()

def test_create_account_missing_password():
    db_reset()
    assert create_account('username="test" name="test" status="test"') is False
    db_reset()

def test_create_account_missing_name():
    db_reset()
    assert create_account('username="test" password="password123" status="test"') is False
    db_reset()

def test_create_account_missing_status():
    db_reset()
    assert create_account('username="test" password="password123" name="test"') is False
    db_reset()

def test_delete_account_existing():
    vali_and_creat_account('deleteuser', 'password123', 'Delete User', 'active')
    account = get_account_by_username('deleteuser')
    assert account is not False
    delete_account(account.session_token)
    account = get_account_by_username('deleteuser')
    assert account is False

def test_delete_account_nonexistent(capsys):
    delete_account('nonexistentsessiontoken')
    captured = capsys.readouterr()
    assert "invalid request: invalid session token" in captured.out
    assert "home: ./app" in captured.out

def test_logout_account_valid():
    db_reset()
    vali_and_creat_account('logoutuser', 'password123', 'Logout User', 'active')
    account = get_account_by_username('logoutuser')
    assert account is not False
    logout_account(account.session_token)
    assert session_token_in_db(account.session_token) is False
    db_reset()

def test_logout_account_invalid_session(capsys):
    db_reset()
    logout_account('nonexistentsessiontoken')
    captured = capsys.readouterr()
    assert "invalid request: invalid session token" in captured.out
    assert "home: ./app" in captured.out
    
def test_join_account(monkeypatch):
    inputs = iter(['newuser', 'password123', 'password123', 'New User', 'active'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    join_account()
    account = get_account_by_username('newuser')
    assert account is not False
    assert account.username == 'newuser'

def test_join_account_password_mismatch(monkeypatch, capsys):
    inputs = iter(['newuser', 'password123', 'wrongpassword', 'New User', 'active'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    join_account()
    captured = capsys.readouterr()
    assert "failed to join: passwords do not match" in captured.out
    assert "home: ./app" in captured.out
    account = get_account_by_username('newuser')
    assert account is False
    