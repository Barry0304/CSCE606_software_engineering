from src.main.db import insert_account_to_db,username_in_db,delete_account_from_db,get_account_by_username,get_account_by_session_token,invalidate_session_token
from src.main.account import Account
from src.main.utils import parse_args,is_valid_username
from src.main.info import show_info, show_info_with_account,show_session_token_invalid

def print_account_created_info(account):
    print("\n[account created]")
    show_info_with_account(account)

def print_login_info(account):
    print(
    f"Welcome back to the App, {account.name}!\n\n"
    f"\"{account.status}\"\n\n"
    f"edit: ./app 'session {account.session_token} edit'\n"
    f"update: ./app 'session {account.session_token} update (name=\"<value>\"|status=\"<value>\")+''\n"
    f"logout: ./app 'session {account.session_token} logout'\n"
    f"people: ./app '[session {account.session_token}] people'"
    )

def print_login_fail_info():
    print("access denied: incorrect username or password")
    print("home: ./app")

def vali_and_creat_account(username,password,name,status):
    if len(username) < 3:
        print("failed to create: username is too short")
    elif len(username) > 20:
        print("failed to create: username is too long")
    elif len(name) < 1:
        print("failed to create: name is too short")
    elif len(name) > 30:
        print("failed to create: name is too long")
    elif len(status) < 1:
        print("failed to create: status is too short")
    elif len(status) > 100:
        print("failed to create: status is too long")
    elif len(password) < 4:
        print("failed to create: password is too short")
    elif '"' in name :
        print("failed to create: name contains double quote")
    elif '"' in status:
        print("failed to create: status contains double quote")
    elif '"' in password:
        print("failed to create: password contains double quote")    
    elif not is_valid_username(username):
        print("failed to create: invalid username")
    elif username_in_db(username):
        print(f"failed to create: {username} is already registered")
        account = get_account_by_username(username)
        print_account_created_info(account)
    else:
        account = Account(username=username.lower(),password=password, name=name, status=status)
        insert_account_to_db(account)
        print_account_created_info(account)

def join_account():
    print("New Person")
    print("----------")
    username = input("username: ")
    password = input("password: ")
    confirm_password = input("confirm password: ")
    name = input("name: ")
    status = input("status: ")
    if password != confirm_password:
        print("failed to join: passwords do not match")
        print("home: ./app")
    else:
        vali_and_creat_account(username,password, name, status)


def create_account(args):
    args_dict = parse_args(args)
    if "username" not in args_dict:
        print("failed to create: missing username")
        return False
    elif "password" not in args_dict:
        print("failed to create: missing password")
        return False
    elif "name" not in args_dict:
        print("failed to create: missing name")
        return False
    elif "status" not in args_dict:
        print("failed to create: missing status")
        return False
    else:
        vali_and_creat_account(args_dict['username'],args_dict['password'], args_dict['name'], args_dict['status'])

    
def delete_account(session_token):
    if delete_account_from_db(session_token):
        print("[account deleted]\n")
        show_info()
    else:
        show_session_token_invalid()

def login_account(args):
    if  len(args)==0:
        print('invalid request: missing username and password')
        print('home: ./app')
        return False
    
    elif len(args.split(" ",1)) == 1:
        print("access denied: incorrect username or password")
        print('home: ./app')
        return False

    else:
        username,password = args.split(" ",1)
        account= get_account_by_username(username)
        if account and (account.password == password):
            print_login_info(account)
        else:
            print_login_fail_info()
            return False

def logout_account(session_token):
    account = get_account_by_session_token(session_token)
    if not account:
        print("invalid request: invalid session token\nhome: ./app\n")
    else:
        account.logout()
        invalidate_session_token(session_token)
        print("[you are now logged out]\n")
        show_info()