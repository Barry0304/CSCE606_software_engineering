import sqlite3
from src.main.utils import load_config
from src.main.account import Account

def load_db():
    config = load_config()
    db_path = config['database']['path']
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn,cursor

def delete_table(cursor):
    cursor.execute('DELETE FROM accounts')

def create_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT,
        name TEXT NOT NULL,
        status TEXT,
        updated TEXT,
        session_token TEXT)
    ''')

def db_reset():
    conn,cursor = load_db()
    if is_table(cursor):
        delete_table(cursor)
    else:
        create_table(cursor)
    closs_db(conn)

def is_table(cursor):
    cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='accounts';
    ''')
    exists = cursor.fetchone()
    return exists

def closs_db(conn):
    conn.commit()
    conn.close()

def insert_account_to_db(account):
    conn,cursor= load_db()
    cursor.execute('''
        INSERT INTO accounts (username, password, name, status, updated, session_token)
        VALUES (?, ?, ?, ?, ?, ?)
        ''',(account.username, account.password, account.name, account.status, account.updated, account.session_token)
    )
    closs_db(conn)

def username_in_db(username):
    conn,cursor= load_db()
    cursor.execute('SELECT * FROM accounts WHERE username = LOWER(?)', (username,))
    exist = cursor.fetchone()
    closs_db(conn)
    return exist

def session_token_in_db(session_token):
    conn,cursor= load_db()
    cursor.execute('SELECT * FROM accounts WHERE session_token = ?', (session_token,))
    exist = cursor.fetchone() is not None
    closs_db(conn)
    return exist

def delete_account_from_db(session_token):
    if not session_token_in_db(session_token):
        return False
    else:
        conn,cursor= load_db()
        cursor.execute('DELETE FROM accounts WHERE session_token = ?', (session_token,))
        closs_db(conn)
        return True

def get_account_by_username(username):
    if not username_in_db(username):
        return False
    conn,cursor= load_db()
    cursor.execute('SELECT * FROM accounts WHERE username = LOWER(?) ', (username,))
    account= Account(*(cursor.fetchone()[1:]))
    closs_db(conn)
    return account

def get_account_by_session_token(session_token):
    if not session_token_in_db(session_token):
        return False
    conn,cursor= load_db()
    cursor.execute('SELECT * FROM accounts WHERE session_token = ?', (session_token,))
    account= Account(*(cursor.fetchone()[1:]))
    closs_db(conn)
    return account

def update_account_to_db(account):
    conn,cursor= load_db()
    cursor.execute(
        '''
        UPDATE accounts
        SET name = ?, status = ?, updated = ?
        WHERE session_token = ?
        ''', (account.name, account.status, account.updated, account.session_token)
    )
    closs_db(conn)

def invalidate_session_token(session_token):
    if not session_token_in_db(session_token):
        return False
    else:
        conn,cursor= load_db()
        cursor.execute('''
            UPDATE accounts
            SET session_token = NULL
            WHERE session_token = ?
        ''', (session_token,))
        closs_db(conn)


def get_all_accounts():
    conn,cursor= load_db()
    cursor.execute('SELECT * FROM accounts')
    rows = cursor.fetchall()
    accounts = []
    for row in rows:
        account= Account(*(row[1:]))
        accounts.append(account)
    closs_db(conn)
    return accounts

def find_in_db(field,value):
    conn, cursor = load_db()
    if value == "":
        cursor.execute('SELECT username, name, status, updated FROM accounts')
    elif field == 'any':
        cursor.execute('''SELECT username, name, status, updated FROM accounts 
                          WHERE username LIKE LOWER(?) OR name LIKE ? OR status LIKE ? OR updated LIKE ?''',
                       (f'%{value}%', f'%{value}%', f'%{value}%', f'%{value}%'))
    else:
        cursor.execute(f'SELECT username, name, status, updated FROM accounts WHERE {field} LIKE ?', (f'%{value}%',))
    
    results = cursor.fetchall()
    closs_db(conn)
    return results

def sort_in_db(field, order):
    conn, cursor = load_db()
    cursor.execute(f'SELECT username, name, status, updated FROM accounts ORDER BY {field} {order.upper()}')
    results = cursor.fetchall()
    closs_db(conn)
    return results