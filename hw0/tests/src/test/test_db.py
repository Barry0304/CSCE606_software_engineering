import pytest
from src.main.db import (
    create_table,
    delete_table,
    session_token_in_db,
    db_reset, closs_db,
    insert_account_to_db,
    get_account_by_username,
    load_db,
    delete_account_from_db,
    update_account_to_db,
    get_account_by_session_token,
    get_account_by_username,
    invalidate_session_token,
    get_all_accounts,
    find_in_db,
    sort_in_db
)

from src.main.account import Account

@pytest.fixture(scope="function")

def test_create_table():
    db_reset()
    conn,cursor = load_db()

    create_table(cursor)##

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts';")
    result = cursor.fetchone()
    assert result is not None
    assert result[0] == "accounts"
    closs_db(conn)
    db_reset()


def test_db_reset_with_existing_table():
    db_reset()
    conn,cursor = load_db()
    cursor.execute("INSERT INTO accounts (username, password, name, status, updated, session_token) VALUES (?, ?, ?, ?, ?, ?)",
                   ('testuser', 'password123', 'Test User', 'active', '2024-01-01 00:00:00', 'sessiontoken123'))
    cursor.execute("SELECT COUNT(*) FROM accounts;")
    result = cursor.fetchone()
    assert result[0] == 1
    closs_db(conn)

    db_reset()##

    conn,cursor = load_db()
    cursor.execute("SELECT COUNT(*) FROM accounts;")
    result = cursor.fetchone()
    assert result[0] == 0
    closs_db(conn)
    db_reset()


def test_db_reset_without_existing_table():
    db_reset()
    conn,cursor = load_db()
    cursor.execute("DROP TABLE IF EXISTS accounts;")
    closs_db(conn)

    db_reset()##

    conn,cursor = load_db()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts';")
    result = cursor.fetchone()
    assert result is not None
    assert result[0] == "accounts"
    db_reset()


def test_delete_table():
    db_reset()
    conn,cursor = load_db()
    create_table(cursor)
    cursor.execute("SELECT COUNT(*) FROM accounts;")
    result = cursor.fetchone()
    assert result[0] == 0
    cursor.execute("INSERT INTO accounts (username, password, name, status, updated, session_token) VALUES (?, ?, ?, ?, ?, ?)",
                   ('testuser', 'password123', 'Test User', 'active', '2024-01-01 00:00:00', 'sessiontoken123'))
    cursor.execute("SELECT COUNT(*) FROM accounts;")
    result = cursor.fetchone()
    assert result[0] == 1

    delete_table(cursor)##

    cursor.execute("SELECT COUNT(*) FROM accounts;")
    result = cursor.fetchone()
    assert result[0] == 0
    closs_db(conn)
    db_reset()

def test_insert_and_retrieve_account():
    db_reset()
    account = Account(username="testuser", password="password123", name="Test User", status="active")
    insert_account_to_db(account)
    retrieved_account = get_account_by_username("testuser")
    assert retrieved_account.username == "testuser"
    db_reset()


def test_delete_account_success():
    db_reset()
    conn,cursor = load_db()
    cursor.execute("INSERT INTO accounts (username, password, name, status, updated, session_token) VALUES (?, ?, ?, ?, ?, ?)",
                   ('testuser', 'password123', 'Test User', 'active', '2024-01-01 00:00:00', 'sessiontoken123'))
    closs_db(conn)

    assert session_token_in_db('sessiontoken123') is not None
    result = delete_account_from_db('sessiontoken123')##

    conn,cursor = load_db()
    assert result is True
    cursor.execute("SELECT * FROM accounts WHERE session_token = ?", ('sessiontoken123',))
    result = cursor.fetchone()
    assert result is None
    closs_db(conn)
    db_reset()

def test_delete_account_failure():
    db_reset()
    conn,cursor = load_db()
    cursor.execute("SELECT COUNT(*) FROM accounts;")
    result = cursor.fetchone()
    assert result[0] == 0
    closs_db(conn)
    result = delete_account_from_db('nonexistentsessiontoken')
    assert result is False
    db_reset()

def test_get_account_by_username_exists():
    db_reset()
    conn, cursor = load_db()
    cursor.execute("INSERT INTO accounts (username, password, name, status, updated, session_token) VALUES (?, ?, ?, ?, ?, ?)",
                   ('testuser', 'password123', 'Test User', 'active', '2024-01-01 00:00:00', 'sessiontoken123'))
    closs_db(conn)

    account = get_account_by_username('testuser')
    assert account is not False
    assert account.username == 'testuser'
    assert account.name == 'Test User'
    db_reset()


def test_get_account_by_username_not_exists():
    db_reset()
    account = get_account_by_username('nonexistentuser')
    assert account is False 

def test_get_account_by_session_token_exists():
    db_reset()
    conn, cursor = load_db()
    cursor.execute("INSERT INTO accounts (username, password, name, status, updated, session_token) VALUES (?, ?, ?, ?, ?, ?)",
                   ('testuser', 'password123', 'Test User', 'active', '2024-01-01 00:00:00', 'sessiontoken123'))
    closs_db(conn)

    account = get_account_by_session_token('sessiontoken123')
    assert account is not False
    assert account.session_token == 'sessiontoken123'
    assert account.name == 'Test User'
    db_reset()

def test_get_account_by_session_token_not_exists():
    db_reset()
    account = get_account_by_session_token('nonexistentsessiontoken')
    assert account is False

def test_update_account():
    account = Account(username="upduser", password="password123", name="Update User", status="active")
    insert_account_to_db(account)
    account.update_name("Updated Name")
    update_account_to_db(account)
    updated_account = get_account_by_username("upduser")
    assert updated_account.name == "Updated Name"
    db_reset()


def test_invalidate_session_token_exists():
    db_reset()
    conn, cursor = load_db()
    cursor.execute("INSERT INTO accounts (username, password, name, status, updated, session_token) VALUES (?, ?, ?, ?, ?, ?)",
                   ('testuser', 'password123', 'Test User', 'active', '2024-01-01 00:00:00', 'sessiontoken123'))
    closs_db(conn)

    account = get_account_by_session_token('sessiontoken123')
    assert account is not False
    assert account.session_token == 'sessiontoken123'
    invalidate_session_token('sessiontoken123')
    account = get_account_by_session_token('sessiontoken123')
    assert account is False
    db_reset()

def test_invalidate_session_token_not_exists():
    db_reset()
    account = invalidate_session_token('nonexistentsessiontoken')
    assert account is False

def test_get_all_accounts():
    db_reset()
    account1 = Account(username="user1", password="password1", name="User One", status="active")
    account2 = Account(username="user2", password="password2", name="User Two", status="inactive")
    insert_account_to_db(account1)
    insert_account_to_db(account2)

    accounts = get_all_accounts()

    assert len(accounts) == 2
    assert accounts[0].username == 'user1'
    assert accounts[1].username == 'user2'
    db_reset()

def test_find_in_db_any_field():
    db_reset()
    account1 = Account(username="user1", password="password1", name="User One", status="active")
    account2 = Account(username="user2", password="password2", name="User Two", status="inactive")
    insert_account_to_db(account1)
    insert_account_to_db(account2)

    results = find_in_db("","")
    assert len(results) == 2

    results = find_in_db('any', 'user')
    assert len(results) == 2

    results = find_in_db('name', 'User One')
    assert len(results) == 1
    assert results[0][0] == 'user1'
    db_reset()

def test_sort_in_db():
    db_reset()
    account1 = Account(username="user1", password="password1", name="User One", status="active", updated="2024-01-01 00:00:00")
    account2 = Account(username="user2", password="password2", name="User Two", status="inactive", updated="2024-01-02 00:00:00")
    insert_account_to_db(account1)
    insert_account_to_db(account2)

    results = sort_in_db('updated', 'asc')
    assert results[0][0] == 'user1'
    assert results[1][0] == 'user2'

    results = sort_in_db('updated', 'desc')
    assert results[0][0] == 'user2'
    assert results[1][0] == 'user1'
    db_reset()
